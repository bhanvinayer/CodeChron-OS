"""
Mutation Engine - Tracks code changes and enables rollbacks
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Any, Optional
import hashlib

class MutationEngine:
    """Tracks and manages code mutations"""
    
    def __init__(self, log_file: str = "data/logs/mutation_history.json"):
        self.log_file = log_file
        self.mutations: List[Dict] = []
        self.current_state: Dict = {}
        self.load_history()
    
    def track_mutation(
        self,
        mutation_type: str,
        description: str,
        code_before: str,
        code_after: str,
        author: str = "User",
        era: str = "unknown",
        metadata: Optional[Dict] = None
    ) -> str:
        """
        Track a code mutation
        
        Args:
            mutation_type: Type of mutation (code, ui, ai, block)
            description: Human-readable description
            code_before: Code before change
            code_after: Code after change
            author: Who made the change
            era: Which era/mode made the change
            metadata: Additional metadata
            
        Returns:
            Mutation ID
        """
        
        mutation_id = self._generate_id()
        
        # Calculate diff stats
        diff_stats = self._calculate_diff(code_before, code_after)
        
        mutation = {
            "id": mutation_id,
            "timestamp": datetime.now().isoformat(),
            "type": mutation_type,
            "description": description,
            "author": author,
            "era": era,
            "code_before": code_before,
            "code_after": code_after,
            "diff_stats": diff_stats,
            "metadata": metadata or {}
        }
        
        self.mutations.append(mutation)
        self.save_history()
        
        return mutation_id
    
    def rollback_to_mutation(self, mutation_id: str) -> Dict[str, Any]:
        """
        Rollback to a specific mutation
        
        Args:
            mutation_id: ID of mutation to rollback to
            
        Returns:
            Result with code state and rollback info
        """
        
        # Find the mutation
        target_mutation = None
        for mutation in self.mutations:
            if mutation["id"] == mutation_id:
                target_mutation = mutation
                break
        
        if not target_mutation:
            return {
                "success": False,
                "error": f"Mutation {mutation_id} not found"
            }
        
        # Get code state at that point
        rollback_code = target_mutation["code_after"]
        
        # Track the rollback as a new mutation
        current_code = self.get_current_code()
        self.track_mutation(
            mutation_type="rollback",
            description=f"Rolled back to: {target_mutation['description']}",
            code_before=current_code,
            code_after=rollback_code,
            author="System",
            era="rollback",
            metadata={"target_mutation_id": mutation_id}
        )
        
        return {
            "success": True,
            "code": rollback_code,
            "mutation": target_mutation,
            "rollback_id": self.mutations[-1]["id"]
        }
    
    def get_mutation_history(
        self,
        limit: Optional[int] = None,
        mutation_type: Optional[str] = None,
        era: Optional[str] = None
    ) -> List[Dict]:
        """
        Get mutation history with optional filtering
        
        Args:
            limit: Maximum number of mutations to return
            mutation_type: Filter by mutation type
            era: Filter by era
            
        Returns:
            List of mutations
        """
        
        filtered_mutations = self.mutations.copy()
        
        # Apply filters
        if mutation_type:
            filtered_mutations = [
                m for m in filtered_mutations 
                if m.get("type") == mutation_type
            ]
        
        if era:
            filtered_mutations = [
                m for m in filtered_mutations
                if m.get("era") == era
            ]
        
        # Sort by timestamp (newest first)
        filtered_mutations.sort(
            key=lambda m: m.get("timestamp", ""),
            reverse=True
        )
        
        # Apply limit
        if limit:
            filtered_mutations = filtered_mutations[:limit]
        
        return filtered_mutations
    
    def get_mutation_stats(self) -> Dict[str, Any]:
        """Get statistics about mutations"""
        
        total_mutations = len(self.mutations)
        
        # Count by type
        type_counts = {}
        era_counts = {}
        author_counts = {}
        
        for mutation in self.mutations:
            # Type counts
            mut_type = mutation.get("type", "unknown")
            type_counts[mut_type] = type_counts.get(mut_type, 0) + 1
            
            # Era counts
            era = mutation.get("era", "unknown")
            era_counts[era] = era_counts.get(era, 0) + 1
            
            # Author counts
            author = mutation.get("author", "unknown")
            author_counts[author] = author_counts.get(author, 0) + 1
        
        # Calculate total lines changed
        total_lines_added = sum(
            m.get("diff_stats", {}).get("lines_added", 0)
            for m in self.mutations
        )
        
        total_lines_removed = sum(
            m.get("diff_stats", {}).get("lines_removed", 0)
            for m in self.mutations
        )
        
        return {
            "total_mutations": total_mutations,
            "type_counts": type_counts,
            "era_counts": era_counts,
            "author_counts": author_counts,
            "lines_added": total_lines_added,
            "lines_removed": total_lines_removed,
            "net_lines": total_lines_added - total_lines_removed
        }
    
    def export_mutations(self, format: str = "json") -> str:
        """Export mutations in specified format"""
        
        if format == "json":
            return json.dumps(self.mutations, indent=2)
        
        elif format == "csv":
            import csv
            import io
            
            output = io.StringIO()
            writer = csv.writer(output)
            
            # Header
            writer.writerow([
                "ID", "Timestamp", "Type", "Description", 
                "Author", "Era", "Lines Added", "Lines Removed"
            ])
            
            # Data
            for mutation in self.mutations:
                diff_stats = mutation.get("diff_stats", {})
                writer.writerow([
                    mutation.get("id", ""),
                    mutation.get("timestamp", ""),
                    mutation.get("type", ""),
                    mutation.get("description", ""),
                    mutation.get("author", ""),
                    mutation.get("era", ""),
                    diff_stats.get("lines_added", 0),
                    diff_stats.get("lines_removed", 0)
                ])
            
            return output.getvalue()
        
        else:
            raise ValueError(f"Unsupported export format: {format}")
    
    def load_history(self):
        """Load mutation history from file"""
        
        if os.path.exists(self.log_file):
            try:
                with open(self.log_file, 'r') as f:
                    data = json.load(f)
                    self.mutations = data.get("mutations", [])
                    self.current_state = data.get("current_state", {})
            except (json.JSONDecodeError, IOError):
                self.mutations = []
                self.current_state = {}
    
    def save_history(self):
        """Save mutation history to file"""
        
        # Ensure directory exists
        os.makedirs(os.path.dirname(self.log_file), exist_ok=True)
        
        data = {
            "mutations": self.mutations,
            "current_state": self.current_state,
            "last_updated": datetime.now().isoformat()
        }
        
        try:
            with open(self.log_file, 'w') as f:
                json.dump(data, f, indent=2)
        except IOError as e:
            print(f"Error saving mutation history: {e}")
    
    def get_current_code(self) -> str:
        """Get current code state"""
        
        if self.mutations:
            return self.mutations[-1].get("code_after", "")
        return ""
    
    def _generate_id(self) -> str:
        """Generate unique mutation ID"""
        
        timestamp = datetime.now().isoformat()
        return hashlib.md5(timestamp.encode()).hexdigest()[:8]
    
    def _calculate_diff(self, code_before: str, code_after: str) -> Dict[str, int]:
        """Calculate diff statistics between two code versions"""
        
        lines_before = code_before.split('\n') if code_before else []
        lines_after = code_after.split('\n') if code_after else []
        
        # Simple line-based diff (in real implementation, use difflib)
        lines_added = max(0, len(lines_after) - len(lines_before))
        lines_removed = max(0, len(lines_before) - len(lines_after))
        
        # Calculate changed lines (approximation)
        common_lines = min(len(lines_before), len(lines_after))
        lines_modified = 0
        
        for i in range(common_lines):
            if lines_before[i] != lines_after[i]:
                lines_modified += 1
        
        return {
            "lines_added": lines_added,
            "lines_removed": lines_removed,
            "lines_modified": lines_modified,
            "total_changes": lines_added + lines_removed + lines_modified
        }
    
    def find_similar_mutations(self, description: str, limit: int = 5) -> List[Dict]:
        """Find mutations with similar descriptions"""
        
        import difflib
        
        matches = difflib.get_close_matches(
            description,
            [m.get("description", "") for m in self.mutations],
            n=limit,
            cutoff=0.6
        )
        
        similar_mutations = []
        for match in matches:
            for mutation in self.mutations:
                if mutation.get("description") == match:
                    similar_mutations.append(mutation)
                    break
        
        return similar_mutations

# Global instance
mutation_engine = MutationEngine()
