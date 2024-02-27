jQuery(function () {
    const $emailInput = $("#id_email");
    const $cnpjInput = $("#id_cnpj");
    const $phoneInput = $("#id_phone");
    const $zipcodeInput = $("#zipcodeInput");

    $zipcodeInput.mask("00000-000");
    $cnpjInput.mask("00.000.000/0000-00");
    $phoneInput.mask("(00) 0 0000-0000");
    
    // Placeholder Style
    $cnpjInput.addClass("placeholderStyle");
    $cnpjInput.attr("placeholder", "00.000.000/0000-00")
    $emailInput.addClass("placeholderStyle");
    $emailInput.attr("placeholder", "exemple@email.com")
    $phoneInput.addClass("placeholderStyle");
    $phoneInput.attr("placeholder", "(99) 9 9999-9999")})