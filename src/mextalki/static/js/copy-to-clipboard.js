let button_id = '#cp-to-clipboard';
let button = $(button_id);

button.tooltip({
  trigger: 'click',
});

let clipboard = new Clipboard(button_id);

function setTooltip(message) {
  button.tooltip('hide')
    .attr('data-original-title', message)
    .tooltip('show');
}

function hideTooltip() {
  setTimeout(function() {
    button.tooltip('hide');
  }, 1000);
}

clipboard.on('success', function(e) {
  setTooltip('Copied!');
  hideTooltip();
});

clipboard.on('error', function(e) {
  setTooltip('Failed!');
  hideTooltip();
});
