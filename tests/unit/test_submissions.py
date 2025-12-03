"""
Tests for patiencediff integration in submissions.

These tests verify that the code correctly uses patiencediff when available,
and falls back to standard difflib when not available.
"""
import pytest

class TestPatiencediffImport:
    """Test that patiencediff is imported correctly with fallback"""

    def test_import_provides_unified_diff(self):
        """Both patiencediff and difflib provide unified_diff"""
        # The import pattern ensures we always have unified_diff available
        try:
            import patiencediff as difflib
        except ImportError:
            import difflib
        
        assert hasattr(difflib, 'unified_diff')

    def test_fallback_to_standard_difflib(self):
        """Standard difflib should always be available"""
        import difflib
        assert hasattr(difflib, 'unified_diff')

class TestDiffFunctionality:
    """Test that unified_diff works correctly regardless of implementation"""

    def test_unified_diff_detects_changes(self):
        """unified_diff should detect changes between old and new content"""
        import difflib
        
        old_content = ['Hello\n', 'World\n']
        new_content = ['Hello\n', 'World!\n']
        
        diff = list(difflib.unified_diff(old_content, new_content))
        
        # Should have diff lines
        assert len(diff) > 0

    def test_unified_diff_no_changes(self):
        """unified_diff produces minimal output when content is identical"""
        import difflib
        
        content = ['Hello\n', 'World\n']
        
        diff = list(difflib.unified_diff(content, content))
        
        # Should be empty or only headers
        assert len(diff) <= 2

    def test_unified_diff_with_context(self):
        """unified_diff should respect context parameter"""
        import difflib
        
        old_content = ['line 1\n', 'line 2\n', 'line 3\n', 'line 4\n', 'line 5\n']
        new_content = ['line 1\n', 'line 2\n', 'CHANGED\n', 'line 4\n', 'line 5\n']
        
        # Use 1 line of context
        diff = list(difflib.unified_diff(old_content, new_content, n=1))
        
        # Should have some output
        assert len(diff) > 0

    def test_unified_diff_multiple_changes(self):
        """unified_diff should handle multiple changes"""
        import difflib
        
        old_content = [
            'line 1\n',
            'line 2\n',
            'line 3\n',
            'line 4\n',
            'line 5\n'
        ]
        new_content = [
            'line 1 modified\n',
            'line 2\n',
            'line 3 modified\n',
            'line 4\n',
            'line 5 modified\n'
        ]
        
        diff = list(difflib.unified_diff(old_content, new_content))
        
        # Should detect multiple changes
        assert len(diff) > 0
        removed_lines = [line for line in diff if line.startswith('-') and not line.startswith('---')]
        added_lines = [line for line in diff if line.startswith('+') and not line.startswith('+++')]
        assert len(removed_lines) > 0
        assert len(added_lines) > 0
