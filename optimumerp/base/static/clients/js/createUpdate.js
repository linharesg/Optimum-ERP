jQuery(function () {
    const $form = $("form");
    const $emailInput = $("#id_email");
    const $streetInput = $("#id_street");
    const $numberInput = $("#id_number");
    const $cityInput = $("#id_city");
    const $stateInput = $("#id_state");
    const $cnpjInput = $("#id_cnpj");
    const $phoneInput = $("#id_phone");
    const $zipcodeInput = $("#zipcodeInput");
    const $zipcodeIcon = $("#zipcodeIcon");

    console.log("funcionou")

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

    // Acrescentando as validações para o formulário: https://jqueryvalidation.org/validate/
    $form.validate({
        errorElement: "div", // Elemento que será criado
        errorClass: "invalid-feedback", // Classe que será aplicada
        // Como os campos com erro irão se comportar
        highlight: (element, _, validClass) => {
            $(element).addClass("is-invalid");
        },
        // Como os campos sem erro irão se comportar
        unhighlight: (element) => {
            $(element).removeClass("is-invalid");
        },
        // Onde a mensagem de erro será adicionada
        errorPlacement: (error, element) => {
            error.addClass("invalid-feedback");
            if (element.prop("id") === "id_zipcode") { // Caso seja o campo do CEP
                error.insertAfter(element.next()); // Inserir depois do ícone
            } else {
                error.insertAfter(element);
            }
        },
        // Validações que serão aplicadas
        rules: {
            company_name: {
                required: true,
            },
            fantasy_name: {
                required: true,
            },
            phone: {
                required: true,
                minlength: 16,
            },
            representative: {
                required: true,
                minlength: 3,
            },
            cnpj: {
                required: true,
                minlength: 18,
            },
            email: {
                required: true,
            },
            zipcode: {
                required: true,
                minlength: 9,
            },
            street: {
                required: true,
            },
            number: {
                required: true,
            },
            city: {
                required: true,
            },
            state: {
                required: true,
            },
        },
        // Mensagens que serão exibidas de acordo com os erros
        messages: {
            company_name: "Por favor, informe a razão social",
            representative: "Por favor, informe o nome do representante",
            fantasy_name: "Por favor, informe o nome fantasia",
            phone: {
                required: "Por favor, informe o telefone",
                minlength: "Informe um telefone válido"
            },

            name: {
                required: "Por favor, insira o nome do representante",
                minlength: "O nome do representante deve ter no mínimo 3 caracteres",
            },
            cnpj: {
                required: "Por favor, insira um CNPJ",
                minlength: "CNPJ inválido."
            },
            email: {
                required: "Por favor, insira o E-mail"
            },
            zipcode: {
                required: "Por favor, insira um CEP válido",
                minlength: "Informe um CEP Válido"
            },
            street: "Por favor, insira um endereço válido",
            number: "Por favor, insira um número válido",
            city: "Por favor, insira uma cidade",
            state: "Por favor, insira um estado"
        },
    });
});