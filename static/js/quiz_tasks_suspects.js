$(document).ready(function () {
    $('#suspects').addClass('d-none');

    $('.tab-btn').click(function () {
      var target = $(this).text().toLowerCase();

      // Toggle tab button state
      $('.tab-btn').removeClass('active');
      $(this).addClass('active');

      // Toggle tab button content
      $('.tab-panel').removeClass('d-block');
      $('.tab-panel').removeClass('d-none');
      if (target == "tasks") {
        $('#tasks').addClass('d-block');
        $('#suspects').addClass('d-none');
      } else {
        $('#suspects').addClass('d-block');
        $('#tasks').addClass('d-none');
      }
    });
});