jQuery(function () {
    const $emailInput = $("#id_email");
    const $streetInput = $("#id_street");
    const $numberInput = $("#id_number");
    const $cityInput = $("#id_city");
    const $stateInput = $("#id_state");
    const $cnpjInput = $("#id_cnpj");
    const $phoneInput = $("#id_phone");
    const $zipcodeInput = $("#zipcodeInput");
    const $zipcodeIcon = $("#zipcodeIcon");

    $zipcodeInput.mask("00000-000");
    $cnpjInput.mask("00.000.000/0000-00");
    $phoneInput.mask("(00) 0 0000-0000");
    
    // Placeholder Style
    $cnpjInput.addClass("placeholderStyle");
    $cnpjInput.attr("placeholder", "00.000.000/0000-00")
    $emailInput.addClass("placeholderStyle");
    $emailInput.attr("placeholder", "exemple@email.com")
    $phoneInput.addClass("placeholderStyle");
    $phoneInput.attr("placeholder", "(99) 9 9999-9999")

    // Adicionando o manipulador do evento "blur" para o input de CEP
    $zipcodeInput.on("blur", function () {
        // Valor do CEP digitado
        const zipcode = $(this).val().replace("-", "");

        // Se nenhum CEP tiver sido digitado não realizar a requisição
        if (zipcode.length !== 8) return;

        // Mudando o ícone do CEP
        $zipcodeIcon.attr("class", "spinner-border spinner-border-sm");

        // Realiza uma solicitação GET para a API viacep.com.br usando o CEP informado
        fetch(`https://viacep.com.br/ws/${zipcode}/json/`)
            .then(res => res.json()) // Obtendo somento os dados da requisição
            .then(data => {
                if (!data.erro) { // Verificando se o site existe
                    // Preenchendo os inputs com os valores da API
                    $streetInput.val(data.logradouro);
                    $cityInput.val(data.localidade);
                    $stateInput.val(data.uf);

                    // Focando o input de número
                    $numberInput.focus();
                }
            })
            .catch(() => console.error("Falha ao realizar a requisição para a API do VIACEP"))
            .finally(() => $zipcodeIcon.attr("class", "bi bi-geo-alt"));
    });
})