jQuery(function() {
    const $form = $("#sales_order_form");
    const $submitButton = $("#submitButton");
    const $addButton = $("#addSaleOrderButton");
    const $productsContainer = $("#productFormset");
    const $totalProducts = $("#id_salesorderproduct_set-TOTAL_FORMS");
    const $originalProduct = $productsContainer.children(".row:first").clone(true);

    $addButton.on("click", function() {
        const $newRow = $originalProduct.clone(true);
        const index = parseInt($totalProducts.val());

        $newRow.find(":input[name]").each(function() {
            const name = $(this).attr("name").replace("-0-", `-${index}-`);
            const id = "id_" + name;

            $(this).attr({name, id}).val("");
        });

        $newRow.find('select').on('change', function() {
            const selectedProductId = $(this).val();
            const $allSelects = $productsContainer.find('select');

            const duplicate = $allSelects.filter(function() {
                return $(this).val() === selectedProductId;
            }).length > 1;

            if (duplicate) {
                alert('Este produto já consta no pedido de venda!');
                $(this).val('');
            }
        });

        $totalProducts.val(index + 1);
        $productsContainer.append($newRow);
    });

    $productsContainer.on("click", ".remove-btn", function(){
        const $button = $(this);

        $button.closest(".row").remove();
        $totalProducts.val(parseInt($totalProducts.val()) - 1);

        const url = $button.data("url");
        if (url) {
            fetch(url, {
                method: "POST",
                headers: {
                    "X-CSRFToken": Cookies.get("csrftoken")
                }
            })
            .catch(console.error)
        }
    })

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
            error.insertAfter(element);
        },
        // Validações que serão aplicadas
        rules: {

            installments: {
                required: true,
                max: 36,
            },
            discount: {
                min: 0,
                max: 99,
            },
            total_value: {
                required: true,
            },
        },
        // Mensagens que serão exibidas de acordo com os erros
        messages: {

            installments: "Informe um valor válido.",
            client: "Por favor, informe o cliente.",
            discount: "Por favor, informe um valor válido.",
            total_value: "Por favor, informe um valor válido.",

        },
    });

    $submitButton.on("click", function() {

        const productSelects = document.querySelectorAll('select[name^="salesorderproduct_set"]');

        for (let select of productSelects) {
            if (select.value !== "") {
                return
            }
        }

        event.preventDefault()
        alert('Informe ao menos um produto!')
        return

        });

})
