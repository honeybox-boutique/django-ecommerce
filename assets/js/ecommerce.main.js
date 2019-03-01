$(document).ready(function(){

var stripeFormModule = $(".stripe-payment-form")
var stripeModuleToken = stripeFormModule.attr("data-token")
var stripeModuleNextUrl = stripeFormModule.attr("data-next-url")
var stripeModuleBtnTitle = stripeFormModule.attr("data-btn-title") || "Add Card"

var stripeTemplate = $.templates("#stripeTemplate")
var stripeTemplateDataContext = {
  publishKey: stripeModuleToken,
  nextUrl: stripeModuleNextUrl,
  btnTitle: stripeModuleBtnTitle
}
var stripeTemplateHtml = stripeTemplate.render(stripeTemplateDataContext)
stripeFormModule.html(stripeTemplateHtml)




var paymentForm = $(".payment-form")

if (paymentForm.length > 1){
    alert("Only one payment form is allowed per page")
    paymentForm.css('display', 'none')
}
else if (paymentForm.length == 1){

var pubKey = paymentForm.attr('data-token')
var nextUrl = paymentForm.attr('data-next-url')
var stripe = Stripe(pubKey);

// Create an instance of Elements.
var elements = stripe.elements();

// Custom styling can be passed to options when creating an Element.
// (Note that this demo uses a wider set of styles than the guide below.)
var style = {
  base: {
    color: '#32325d',
    lineHeight: '18px',
    fontFamily: '"Helvetica Neue", Helvetica, sans-serif',
    fontSmoothing: 'antialiased',
    fontSize: '16px',
    '::placeholder': {
      color: '#aab7c4'
    }
  },
  invalid: {
    color: '#fa755a',
    iconColor: '#fa755a'
  }
};

// Create an instance of the card Element.
var card = elements.create('card', {style: style});

// Add an instance of the card Element into the `card-element` <div>.
card.mount('#card-element');

// Handle real-time validation errors from the card Element.
card.addEventListener('change', function(event) {
  var displayError = document.getElementById('card-errors');
  if (event.error) {
    displayError.textContent = event.error.message;
  } else {
    displayError.textContent = '';
  }
});

// Handle form submission.
var form = document.getElementById('payment-form');
form.addEventListener('submit', function(event) {
  event.preventDefault();

  stripe.createToken(card).then(function(result) {
    if (result.error) {
      // Inform the user if there was an error.
      var errorElement = document.getElementById('card-errors');
      errorElement.textContent = result.error.message;
    } else {
      // Send the token to your server.
      stripeTokenHandler(nextUrl, result.token);
    }
  });
});

// Submit the form with the token ID.
function stripeTokenHandler(nextUrl, token) {
    var paymentMethodEndpoint = "/billing/payment-method/create/"

      var addressName = $(".data-addressName").val()
      var addressLine1 = $(".data-addressLine1").val()
      var addressLine2 = $(".data-addressLine2").val()
      var addressCity = $(".data-addressCity").val()
      var addressCountry = $(".data-addressCountry").val()
      var addressState = $(".data-addressState").val()
      var addressPostalCode = $(".data-addressPostalCode").val()
      var $rememberAddress = $("input[name=remember_address]:checked")
      if ($rememberAddress.length != 0){
        var data = {
            'token': token.id,
            'addressName': addressName,
            'addressLine1': addressLine1,
            'addressLine2': addressLine2,
            'addressCity': addressCity,
            'addressCountry': addressCountry,
            'addressState': addressState,
            'addressPostalCode': addressPostalCode,
            'remember_address': 'True',
        }
      } else {
        var data = {
            'token': token.id,
            'addressName': addressName,
            'addressLine1': addressLine1,
            'addressLine2': addressLine2,
            'addressCity': addressCity,
            'addressCountry': addressCountry,
            'addressState': addressState,
            'addressPostalCode': addressPostalCode,
            'remember_address': 'False',
        }
      }
    $.ajax({
        data: data,
        url: paymentMethodEndpoint,
        method: "POST",
        success: function(data){
            var successMsg = data.message || 'Success! Your card was added.'
            card.clear()
            if (nextUrl) {
              window.location.href= nextUrl
            } else {
              window.location.reload()
            }
        },
        error: function(error){
            console.log(error)
        }
    })
}
}
})