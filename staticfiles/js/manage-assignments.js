/**
 * Manage Assignments - Delete and Deactivate Confirmation
 * Handles assignment deactivation and permanent deletion modals
 */

(function() {
    'use strict';
    
    /**
     * Show deactivation confirmation modal
     * @param {string} assignmentName - Name of the assignment to deactivate
     * @param {string} url - URL for deactivation action
     */
    function confirmDeactivate(assignmentName, url) {
        const nameElement = document.getElementById('assignmentNameDeactivate');
        const formElement = document.getElementById('deactivateForm');
        
        if (!nameElement || !formElement) {
            console.error('Modal elements not found');
            return;
        }
        
        nameElement.textContent = assignmentName;
        formElement.action = url;
        
        const modalElement = document.getElementById('deactivateModal');
        if (modalElement) {
            const modal = new bootstrap.Modal(modalElement);
            modal.show();
        }
    }

    /**
     * Show permanent delete confirmation modal
     * @param {string} assignmentName - Name of the assignment to delete permanently
     * @param {string} url - URL for delete action
     */
    function confirmDelete(assignmentName, url) {
        const nameElement = document.getElementById('assignmentNameDelete');
        const formElement = document.getElementById('deleteForm');
        
        if (!nameElement || !formElement) {
            console.error('Modal elements not found');
            return;
        }
        
        nameElement.textContent = assignmentName;
        formElement.action = url;
        
        const modalElement = document.getElementById('deleteModal');
        if (modalElement) {
            const modal = new bootstrap.Modal(modalElement);
            modal.show();
        }
    }

    // Initialize when DOM is ready
    document.addEventListener('DOMContentLoaded', function() {
        console.log('✅ Manage Assignments script loaded successfully');
        
        // Attach event listeners to deactivate buttons
        const deactivateButtons = document.querySelectorAll('.btn-deactivate');
        deactivateButtons.forEach(button => {
            button.addEventListener('click', function() {
                const assignmentName = this.getAttribute('data-assignment-name');
                const assignmentUrl = this.getAttribute('data-assignment-url');
                confirmDeactivate(assignmentName, assignmentUrl);
            });
        });
        
        // Attach event listeners to delete buttons
        const deleteButtons = document.querySelectorAll('.btn-delete');
        deleteButtons.forEach(button => {
            button.addEventListener('click', function() {
                const assignmentName = this.getAttribute('data-assignment-name');
                const assignmentUrl = this.getAttribute('data-assignment-url');
                confirmDelete(assignmentName, assignmentUrl);
            });
        });
        
        console.log(`📋 Found ${deactivateButtons.length} deactivate buttons and ${deleteButtons.length} delete buttons`);
        
        // Handle deactivate modal close
        const deactivateModal = document.getElementById('deactivateModal');
        if (deactivateModal) {
            deactivateModal.addEventListener('hidden.bs.modal', function () {
                const form = document.getElementById('deactivateForm');
                if (form) form.reset();
            });
        }

        // Handle delete modal close
        const deleteModal = document.getElementById('deleteModal');
        if (deleteModal) {
            deleteModal.addEventListener('hidden.bs.modal', function () {
                const form = document.getElementById('deleteForm');
                if (form) form.reset();
            });
        }
    });
})();


