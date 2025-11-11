(function($) {
    'use strict';
    
    function togglePortfolioFields() {
        var portfolioType = $('#id_portfolio_type').val();
        var $onlineFields = $('.online-fields').closest('fieldset');
        var $offlineFields = $('.offline-fields').closest('fieldset');
        
        if (portfolioType === 'online') {
            $onlineFields.show();
            $offlineFields.hide();
        } else if (portfolioType === 'offline') {
            $onlineFields.hide();
            $offlineFields.show();
        }
    }
    
    $(document).ready(function() {
        $('#id_portfolio_type').on('change', togglePortfolioFields);
        togglePortfolioFields();
    });
    
    // Also handle when Django admin adds new inline forms
    django.jQuery(document).on('formset:added', function() {
        togglePortfolioFields();
    });
})(django.jQuery);

