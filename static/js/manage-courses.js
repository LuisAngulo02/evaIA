/**
 * Manage Courses - Delete Confirmation
 * Handles course deletion modal
 */

/**
 * Show delete confirmation modal
 * @param {string} courseName - Name of the course to delete
 * @param {string} deleteUrl - URL for delete action
 */
function confirmDelete(courseName, deleteUrl) {
    document.getElementById('courseName').textContent = courseName;
    document.getElementById('deleteForm').action = deleteUrl;
    
    const modal = new bootstrap.Modal(document.getElementById('deleteModal'));
    modal.show();
}
