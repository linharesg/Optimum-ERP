jQuery(function() {
    const $form = $("#purchases_form");
    const $submitButton = $("#submitButton");
    const $addButton = $("#addPurchaseButton");
    const $productsContainer = $("#productFormset");
    const $totalProducts = $("#id_purchasesproduct_set-TOTAL_FORMS");
    const $originalProduct = $productsContainer.children(".row:first").clone(true);
    const $totalOrderValue = $("#id_total_value")
    const $initialProducts = $("#id_purchasesproduct_set-INITIAL_FORMS")
    const $discount = $('#id_discount')
    var $productRow = $(".productRow")

    const updateTotalValue = function() {
        const totalValueElements = document.querySelectorAll('.productTotalValue input[type="number"]');
        
        let sum = 0;
        totalValueElements.forEach(element => {
            sum += parseFloat(element.value || 0);
        });
        const $discount = $('#id_discount').val()
        $totalOrderValue.val(((sum * (100 - $discount))/100).toFixed(2))
    };

    const updateFormIndex = function(){
        $(".productRow").each(function(index) {
            $(this).find(":input, select, label, div").each(function() {
                const name = $(this).attr("name")
                const id = $(this).attr("id")
                if (name) {
                    const newName = name.replace(/-\d-/, `-${index}-`)
                    $(this).attr("name", newName)

                }
                if (id) {
                    const newId = id.replace(/-\d-/, `-${index}-`)
                    $(this).attr("id", newId)
                }
            })

        })
    }

    const removeProduct = function(){
        const $button = $(this);
        
        $button.closest(".row").remove();
        $totalProducts.val(parseInt($totalProducts.val()) - 1);
        updateTotalValue();
    

        if (parseInt($initialProducts.val()) > 0 && !($button.attr("data-url").includes("/0/"))) {
            $initialProducts.val(parseInt($initialProducts.val()) -1);
            updateFormIndex()
        };

        const url = $button.data("url");
        if (url) {
            fetch(url, {
                method: "POST",
                headers: {
                    "X-CSRFToken": Cookies.get("csrftoken")
                }
            })
            .catch(console.error);
        }

    };

    const removeButtons = document.querySelectorAll('.removeProductButton');
    removeButtons.forEach(button => {
    button.addEventListener('click', updateTotalValue);
    });

    const onProductChange = function() {
        const selectedProductId = $(this).val();
        const $allSelects = $productsContainer.find('select');
        const $currentProductRow = $(this).closest('.productRow');
        const duplicate = $allSelects.filter(function() {
            return $(this).val() === selectedProductId;
        }).length > 1;

        if (duplicate) {
            alert('Este produto já consta no pedido de compra!');
            $(this).val('');
            return;
        }
    
        var productId = $(this).val();
        $.ajax({
            url: 'get_sale_value/',
            data: {
                'product_id': productId
            },
            dataType: 'json',
            success: function(data) {
                $currentProductRow.find('.productUnitValue input').val(data.sale_price);
            }
        });

    };

    const onAmountChange = function() {

        const $currentProductRow = $(this).closest('.productRow');        
        const $productTotalValue = $currentProductRow.find('.productTotalValue input')

        const $productUnitValue = $currentProductRow.find('.productUnitValue input').val();
        const $productAmount = $currentProductRow.find('.productAmount input').val();
        
        const total = $productUnitValue * $productAmount;
        $productTotalValue.val(total.toFixed(2));
        
        updateTotalValue();
    }

    $productRow.find('select').on('change', onProductChange);
    $productRow.find('.productAmount').on('change', onAmountChange);
    $productRow.find('.productUnitValue').on('change', onAmountChange);
    $productRow.find('.select').on('change', onAmountChange);
    $discount.on('change', onAmountChange);

    $addButton.on("click", function() {
        const $newRow = $originalProduct.clone(true);
        const index = parseInt($totalProducts.val());
 
        $newRow.find(":input[name]").each(function() {
            const name = $(this).attr("name").replace("-0-", `-${index}-`);
            const id = "id_" + name;

            $(this).attr({name, id}).val("");
            $(this).find('option').removeAttr('selected');
        });

        $newRow.find("div>div[id]").each(function() {
            const id = $(this).attr("id").replace("-0-", `-${index}-`)
            $(this).attr({ id }).val("");
        });

        $newRow.find("button[data-url").each(function() {
            const oldUrl = $(this).attr("data-url");
            const newUrl = oldUrl.replace(/\d+/, '0');
            $(this).attr("data-url", newUrl).val("");
        });

        $newRow.find('select').on('change', onProductChange);
        $newRow.find('.productAmount').on('change', onAmountChange);
        $newRow.find('.productUnitValue').on('change', onAmountChange);
        $newRow.find('.select').on('change', onAmountChange);

        $totalProducts.val(index + 1);
        $productsContainer.append($newRow);
    });

    $productsContainer.on("click", ".remove-btn", removeProduct)

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

        const productSelects = document.querySelectorAll('select[name^="purchasesproduct_set"]');

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