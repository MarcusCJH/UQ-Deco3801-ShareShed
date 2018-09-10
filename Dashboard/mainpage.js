Chart.defaults.global.legend.display = false;
var ctx = document.getElementById("newMembers").getContext('2d');
var newMembers = new Chart(ctx, {
    type: 'bar',
    data: {
        labels: ["Sept 18", "Aug 18", "Jul 18", "Jun 18", "May 18", "Apr 18"],
        datasets: [{
            label: '# of Members',
            data: [12, 8, 7, 7, 9, 7],
            backgroundColor:
                'rgba(255, 99, 132, 0.2)',
            borderColor:
                'rgba(255,99,132,1)',
            borderWidth: 1
        }]
    },
    options: {
        scales: {
            yAxes: [{
                ticks: {
                    beginAtZero:true
                }
            }]
        }
    }
});


var ctx = document.getElementById("memberships").getContext('2d');
var memberships =new Chart(ctx,{type:"line",
data:{
  labels:["Sept 18", "Aug 18", "Jul 18", "Jun 18", "May 18", "Apr 18"],
  datasets:[{
    label:"Total Memberships",
    data:[65,59,80,81,56,55],
    fill:false,
    borderColor:"rgb(75, 192, 192)",
    lineTension:0.1}]},
    showLine:true,
    options:{scales: {
        yAxes: [{
            ticks: {
                beginAtZero:true
            }
        }]
    }}});



var ctx = document.getElementById("loans").getContext('2d');
var loans = new Chart(ctx, {
    type: 'bar',
    data: {
        labels: ["Sept 18", "Aug 18", "Jul 18", "Jun 18", "May 18", "Apr 18"],
        datasets: [{
            label: '# of Loans',
            data: [50, 42, 49, 50, 42, 38],
            backgroundColor:
                'rgba(255, 206, 86, 0.2)',

            borderColor:
                'rgba(255, 206, 86, 1)',

            borderWidth: 1
        }]
    },
    options: {
        scales: {
            yAxes: [{
                ticks: {
                    beginAtZero:true
                }
            }]
        }
    }
});

var ctx = document.getElementById("newItems").getContext('2d');
var newItems = new Chart(ctx, {
    type: 'bar',
    data: {
        labels: ["Sept 18", "Aug 18", "Jul 18", "Jun 18", "May 18", "Apr 18"],
        datasets: [{
            label: '# of New Items',
            data: [10, 14, 8, 11, 5, 12],
            backgroundColor: 
                'rgba(153, 102, 255, 0.2)',

            borderColor:
                'rgba(153, 102, 255, 1)',

            borderWidth: 1
        }]
    },
    options: {
        scales: {
            yAxes: [{
                ticks: {
                    beginAtZero:true
                }
            }]
        }
    }
});


var ctx = document.getElementById("totalItems").getContext('2d');
var totalItems =new Chart(ctx,{type:"line",
data:{
  labels:["Sept 18", "Aug 18", "Jul 18", "Jun 18", "May 18", "Apr 18"],
  datasets:[{
    label:"Total Items",
    data:[236,231,220,217,215,201],
    fill:false,
    borderColor:'rgba(255, 159, 64, 1)',
    lineTension:0.1}]},
    showLine:true,
    options:{scales: {
        yAxes: [{
            ticks: {
                beginAtZero:true
            }
        }]
    }}});

var barChartData = {
			labels: ["Sept 18", "Aug 18", "Jul 18", "Jun 18", "May 18", "Apr 18"],
			datasets: [{
				label: 'Memberships',
				backgroundColor: 'rgba(255, 99, 132, 0.2)',
        borderColor: 'rgba(255,99,132,1)',
        borderWidth: 1,
				data: [80, 0, 80, 80, 80, 0]
			}, {
				label: 'Others',
				backgroundColor: 'rgba(54, 162, 235, 0.2)',
        borderColor:'rgba(54, 162, 235, 1)',
        borderWidth: 1,
				data: [30, 20, 25, 10, 20, 10]
			}]
		};
		window.onload = function() {
			var ctx = document.getElementById('canvas').getContext('2d');
			window.myBar = new Chart(ctx, {
				type: 'bar',
				data: barChartData,
				options: {
					title: {
						display: false
					},
					tooltips: {
						mode: 'index',
						intersect: false
					},
					responsive: true,
					scales: {
						xAxes: [{
							stacked: true
						}],
						yAxes: [{
							stacked: true
						}]
					}
				}
			});
		};
