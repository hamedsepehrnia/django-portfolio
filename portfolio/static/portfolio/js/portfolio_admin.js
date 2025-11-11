(function($) {
    'use strict';
    
    function togglePortfolioFields() {
        var portfolioType = $('#id_portfolio_type').val();
        var $onlineFields = $('.online-fields');
        var $offlineFields = $('.offline-fields');
        
        if (portfolioType === 'online') {
            $onlineFields.show();
            $offlineFields.hide();
            $('#id_offline_file').closest('.form-row').hide();
        } else if (portfolioType === 'offline') {
            $onlineFields.hide();
            $offlineFields.show();
            $('#id_url').closest('.form-row').hide();
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

