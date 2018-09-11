
$(function() {
$('input[name="datetimes"]').daterangepicker({
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
    startDate: moment().startOf('hour'),
    endDate: moment().startOf('hour').add(24, 'hour'),
    autoApply: true,
    maxSpan: {
        days: 7
    },
    locale: {
      format: ' DD/MM/YY hh:mm A '
    },
    alwaysShowCalendars: true,
}, function(start, end, label) {
  console.log('New date range selected: ' + start.format('DD-MM-YY') + ' to ' + end.format('DD-MM-YY') + ' (predefined range: ' + label + ')');
},
);
});
