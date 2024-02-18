jQuery(function() {
    const $modal = $("#productsModal");

    $modal.on("show.bs.modal", function(e) {
        const $button = $(e.relatedTarget);

        const url = $button.data("url");

        fetch(url)
            .then(response => response.json())
            .then(products => {
                const $productsTableBody = $("#productsTableBody");
                $productsTableBody.empty();

                products.forEach(product => {
                    const $row = $("<tr></tr>");
                    $row.append($("<td>").text(product.name));
                    $row.append($("<td>").text(product.amount));
                    $row.append($("<td>").text(product.total_value));
                    $productsTableBody.append($row);
                })
            })
            .catch(console.error)
    });
});