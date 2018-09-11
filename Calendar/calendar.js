
$(function() {
$('input[name="datetimes"]').daterangepicker({
  autoUpdateInput: false,
  isInvalidDate: function(date) {
    var dateRanges = [
                  { 'start': moment('2018-09-10'), 'end': moment('2018-09-15') },
                  { 'start': moment('2018-10-25'), 'end': moment('2018-10-30') },
              ];
              return dateRanges.reduce(function(bool, range) {
                  return bool || (date >= range.start && date <= range.end);
              }, false);
  },
    timePicker: true,
    timePickerIncrement: 30,
    autoApply: true,
    maxSpan: {
        days: 7
    },
    locale: {
      cancelLabel: 'Clear'
    },
    alwaysShowCalendars: true,
}, function(start, end, label) {
  console.log('New date range selected: ' + start.format('DD-MM-YY') + ' to ' + end.format('DD-MM-YY') + ' (predefined range: ' + label + ')');
},
);
$('input[name="datetimes"]').on('apply.daterangepicker', function(ev, picker) {
      $(this).val(picker.startDate.format('  DD/MM/YY hh:mm A ') + ' - ' + picker.endDate.format(' DD/MM/YY hh:mm A'));
  });

  $('input[name="datetimes"]').on('cancel.daterangepicker', function(ev, picker) {
      $(this).val('');
  });
});
