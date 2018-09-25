$(function() {
$('input[name="datetimes"]').daterangepicker({
    autoUpdateInput: false,
    autoApply: true,
    locale: {
      cancelLabel: 'Clear'
    },
    alwaysShowCalendars: true,
},
 function(start, end, label) {
  console.log('New date range selected: ' + start.format('DD-MM-YY') + ' to ' + end.format('DD-MM-YY') + ' (predefined range: ' + label + ')');
},
);

$('input[name="datetimes"]').on('apply.daterangepicker', function(ev, picker) {
      $(this).val(picker.startDate.format('  DD/MM/YY ') + ' - ' + picker.endDate.format(' DD/MM/YY '));
  });

  $('input[name="datetimes"]').on('cancel.daterangepicker', function(ev, picker) {
      $(this).val('');
  });
});
