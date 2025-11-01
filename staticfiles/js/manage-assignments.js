/**
 * Manage Assignments - Delete Confirmation
 * Handles assignment deletion modal
 */

/**
 * Show delete confirmation modal
 * @param {string} assignmentName - Name of the assignment to delete
 * @param {string} deleteUrl - URL for delete action
 */
function confirmDelete(assignmentName, deleteUrl) {
    document.getElementById('assignmentName').textContent = assignmentName;
    document.getElementById('deleteForm').action = deleteUrl;
    
    const modal = new bootstrap.Modal(document.getElementById('deleteModal'));
    modal.show();
}
