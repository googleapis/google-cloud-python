$('.nav-current').click(function(){
  $('.main-nav').toggleClass('open');
});

$('.faq-btn').click(function(){
  $(this).toggleClass('open');
});

$('.headerlink').parent().each(function() {
  $(this).hover(
    function() { $(this).children('.headerlink').show(); },
    function() { $(this).children('.headerlink').hide(); }
  );
});

$('.side-nav').children('ul:nth-child(2)').children().each(function() {
  var itemName = $(this).text();
    if (itemName !== 'Datastore' &&
        itemName !== 'Storage' &&
        itemName !== 'Pub/Sub' &&
        itemName !== 'Big Query') {
      $(this).css('padding-left','2em');
  }
});

var apiQsSection;
// don't even ask me why
if ($('#cloud-datastore-in-10-seconds').length)
  apiQsSection = $('#cloud-datastore-in-10-seconds');
else if ($('#cloud-storage-in-10-seconds').length)
  apiQsSection = $('#cloud-storage-in-10-seconds');
else if ($('#cloud-pubsub-in-10-seconds').length)
  apiQsSection = $('#cloud-pubsub-in-10-seconds');
else if ($('#cloud-bigquery-in-10-seconds').length)
  apiQsSection = $('#cloud-bigquery-in-10-seconds');

if(apiQsSection) {
  var apiQsSubSections = apiQsSection.children('div');
  var showToggle = $('<span></span>')
      .text('▹')
      .addClass('toggle');
  var hideToggle = $('<span></span>')
      .text('▿')
      .addClass('toggle')
      .hide();
  showToggle.click(function() {
    showToggle.hide();
    hideToggle.show();
    apiQsSubSections.each(function() {
      $(this).show();
    })
  });
  hideToggle.click(function() {
    hideToggle.hide();
    showToggle.show();
    apiQsSubSections.each(function() {
      $(this).hide();
    })
  });
  var toggler = $('<div></div>')
      .addClass('toggler')
      .append(showToggle)
      .append(hideToggle);

  apiQsSubSections.each(function() {
    $(this).hide();
  });
  $(apiQsSection).children('h2').first().prepend(toggler);
}
