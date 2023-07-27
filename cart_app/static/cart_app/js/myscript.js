$('#slider1, #slider2, #slider3, #slider4').owlCarousel({
    loop: true,
    margin: 20,
    responsiveClass: true,
    responsive: {
        0: {
            items: 1,
            nav: false,
            autoplay: true,
        },
        600: {
            items: 3,
            nav: true,
            autoplay: true,
        },
        1000: {
            items: 5,
            nav: true,
            loop: true,
            autoplay: true,
        }
    }
})

$('.plus-cart').click(function() {

    var id = $(this).attr("pid").toString();
    var element = this.parentNode.children[2]
    console.log(id)

    $.ajax({
        type : "GET",
        url: "/plus-to-cart",
        data: {
            prod_id: id
        },
        success: function(data){
            console.log(data)
            element.innerText = data.quantity;
            document.getElementById("total-amount-with-ship").innerText = data.cart_amount;
            document.getElementById("total-amount-without-ship").innerText = data.cart_amount;
        }
    })
})

$('.minus-cart').click(function() {

    var id = $(this).attr("pid").toString();
    var element = this.parentNode.children[2];
    console.log(id)

    $.ajax({
        type : "GET",
        url: "/minus-from-cart",
        data: {
            prod_id: id
        },
        success: function(data){
            console.log(data)
            element.innerText = data.quantity;
            document.getElementById("total-amount-with-ship").innerText = data.cart_amount;
            document.getElementById("total-amount-without-ship").innerText = data.cart_amount;
        }
    })
})

$('.remove-cart').click(function() {

    var id = $(this).attr("pid").toString();
    console.log(id)

    $.ajax({
        type : "GET",
        url: "/remove-from-cart",
        data: {
            prod_id: id
        },
        success: function(data){
            console.log(data)
            document.getElementById("total-amount-with-ship").innerText = data.cart_amount;
            document.getElementById("total-amount-without-ship").innerText = data.cart_amount;
        }
    })
})