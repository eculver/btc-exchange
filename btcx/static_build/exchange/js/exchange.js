/**
 * BTC Exchange Demo JS
 */

(function ($) {

    var CONTENT_CONTAINER = '#exchange-container',
        FORM_CONTAINER = 'form',
        RESULT_CONTAINER = '#result',
        INPUT_CONTAINER = '.control-group',
        ALERT_CONTAINER = '.help-inline',
        INPUT_FIELD = 'input.textinput',
        SUBMIT_BUTTON = 'button[type=submit]',
        LOADING_CLASS = 'loading',
        RESULT_ACTIVE_CLASS = 'active',
        FORM_INVALID_CLASS = 'invalid',
        INPUT_INVALID_CLASS = 'error',

        INPUT_ACTION = 'select',
        INPUT_VALUE = 'input[name=value]',

        ALERT_ACTIVE_CLASS = 'active',
        ALERT_ERROR_CLASS = 'alert-error',
        ALERT_SUCCESS_CLASS = 'alert-success',
        ALERT_TYPES = [ALERT_ERROR_CLASS, ALERT_SUCCESS_CLASS],

        ATTR_DISABLED = 'disabled',
        EVT_SUBMIT = 'submit',
        FORM = 'form',

        ALERT_INVALID = 'Enter a valid decimal value to exchange.';

    function Exchange (config) {
        // stash config
        this.config = config;

        // bind events
        this.bind();
    }

    Exchange.prototype = {
        bind: function () {
            var exchange = this;

            $(CONTENT_CONTAINER).on(EVT_SUBMIT, FORM, function (e) {
                // prevent submit, but don't stop propagation
                e.preventDefault();

                exchange.onExchangeSubmit.call(exchange, e);
            });

            // setup all ajax calls for exchange -- always expect json
            $.ajaxSetup({
                context: exchange,
                dataType: 'json',
                beforeSend: this.beforeSend,
                complete: this.sendComplete
            });
        },

        resultContainer: function () {
            var $container = $(RESULT_CONTAINER);
            this.resultContainer = function () { return $container; };
            return $container;
        },

        showResult: function (value) {
            var $container = this.resultContainer();
            $container.text(this.getResultValue(value));
            $container.addClass(RESULT_ACTIVE_CLASS);
        },

        hideResult: function (value) {
            var $container = this.resultContainer();
            $container.removeClass(RESULT_ACTIVE_CLASS);
        },

        getResultValue: function (value) {
            return "That is worth $" + value.toFixed(2);
        },

        getApiUrl: function (action) {
            return "/" + action;
        },

        onExchangeSubmit: function (e) {
            var form = $(e.target),
                action = $(INPUT_ACTION).val(),
                value = $(INPUT_VALUE).val(),
                url = [this.getApiUrl(action), value].join('/');

            if (this.validate(form)) {
                $.get(url).done(this.onExchangeResponse).fail(this.onExchangeFail);
            }
        },

        onExchangeResponse: function (resp) {
            this.showResult(resp.rate.value);
        },

        onExchangeFail: function (resp) {
            // fail
        },

        beforeSend: function () {
            $(FORM).find(SUBMIT_BUTTON).attr(ATTR_DISABLED, ATTR_DISABLED);
            $(FORM).addClass(LOADING_CLASS);
        },

        sendComplete: function () {
            $(FORM).find(SUBMIT_BUTTON).removeAttr(ATTR_DISABLED);
            $(FORM).removeClass(LOADING_CLASS);
        },

        showAlert: function (text, type) {
            var c = $(ALERT_CONTAINER);
            c.text(text);
            c.addClass(type);
            c.addClass(ALERT_ACTIVE_CLASS);

            // always focus after alert
            this.focus();
        },

        hideAlert: function () {
            var c = $(ALERT_CONTAINER);
            c.removeClass(ALERT_ACTIVE_CLASS);
            c.removeClass(ALERT_TYPES.join(' '));
        },

        showValidationError: function (err) {
            this.showAlert(err, ALERT_ERROR_CLASS);
            $(FORM_CONTAINER).addClass(FORM_INVALID_CLASS);
        },

        hideValidationError: function () {
            var $container = $(FORM_CONTAINER),
                $inputContainers = $container.find(INPUT_CONTAINER);

            this.hideAlert();
            $container.removeClass(FORM_INVALID_CLASS);
            $inputContainers.removeClass(INPUT_INVALID_CLASS);
        },

        focus: function () {
            $("input[type=text]").focus();
        },

        validate: function ($form) {
            var exchange = this,
                isValid = true,
                isFocused = false,
                $inputs = $(INPUT_FIELD);

            // all forms required all fields to be non-empty
            $.each($inputs, function(idx, input) {
                var $input = $(input),
                    value = $.trim($input.val()),
                    $container = $input.parents(INPUT_CONTAINER);

                if (value === '' || isNaN(+value)) {
                    isValid = false;
                    exchange.showValidationError(ALERT_INVALID);
                    $container.addClass(INPUT_INVALID_CLASS);

                    // give focus to first invalid input
                    if (!isFocused) {
                        $input.focus();
                        isFocused = true;
                    }
                }
            });

            return isValid;
        }
    };

    // expose WD.Auth namespace
    window.BTCX = window.WD || {};
    window.BTCX.Exchange = Exchange;
}(jQuery));
