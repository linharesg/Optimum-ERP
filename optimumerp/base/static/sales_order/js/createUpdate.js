jQuery(function() {
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
})
