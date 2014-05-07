$(function () {
    var timeArr = [];
    var speedArr = [];
    var rpmArr = [];
    var accelArr = [];
    var gees = [];

    $.ajax({
        type: "GET",
        url: "/data",
        async: false,
        success : function(res) {
            timeArr = res.timeArr.slice(1, -1);
            speedArr = res.speedArr.slice(1, -1);
            rpmArr = res.rpmArr.slice(1, -1);
            accelArr = res.accelArr60;
            gees = res.gees;
        }
    });
    best060 = 999999999;
    for (var i = 0; i < accelArr.length; i++) {
        if (accelArr[i] < best060)
            best060 = accelArr[i];
    };

    highestGee = 0;
    for (var i = 0; i < gees.length; i++) {
        if (gees[i] > Math.abs(highestGee))
            highestGee = gees[i];
    };

    if (best060 > 1000000)
        $(".sixty").html("N/A")
    else
        $(".sixty").html("" + best060/1000.0 + " seconds")
    $(".gee").html("" + highestGee + "g")

        $('#graph').highcharts({
            chart: {
                zoomType: 'x',
                height: 650
            },
            title: {
                text: 'Engine RPM and Vehicle Speed'
            },
            subtitle: {
                text: 'ODB Carnobi'
            },
            xAxis: {
                categories: timeArr,
                minTickInterval: 75
            },
            yAxis: [{ // Primary yAxis
                title: {
                    text: 'Speed',
                    style: {
                        color: '#89A54E'
                    }
                },
                labels: {
                    formatter: function() {
                        return this.value +'mph';
                    },
                    style: {
                        color: '#89A54E'
                    }
                },
                min: 0,
                max: 70
    
            }, { // Tertiary yAxis
                gridLineWidth: 0,
                title: {
                    text: 'RPM',
                    style: {
                        color: '#AA4643'
                    }
                },
                labels: {
                    formatter: function() {
                        return this.value +' rpm';
                    },
                    style: {
                        color: '#AA4643'
                    }
                },
                opposite: true,
                min: 0,
                max: 7000
            }],
            tickPixelInterval: 100,
            tooltip: {
                shared: true
            },
            legend: {
                layout: 'vertical',
                align: 'left',
                x: 120,
                verticalAlign: 'top',
                y: 80,
                floating: true,
                backgroundColor: '#FFFFFF'
            },
            plotOptions: {
                area: {
                    lineWidth: 1,
                    marker: {
                        enabled: false
                    },
                    shadow: false,
                    states: {
                        hover: {
                            lineWidth: 1
                        }
                    },
                    threshold: null
                },
                series: {
                    turboThreshold: 100000
                }
            },
            tooltip: {
                shared: true,
                formatter: function () {
                    //console.log(this.points[0].point.gearRatio);
                    var p = this.x + '<br />';
                    p += "<span style='color:" + this.points[0].series.color + "''>" + this.points[0].series.name + '</span>: <b>' + this.points[0].y + '</b>';
                    p += "<br />"
                    p += "<span style='color:" + this.points[1].series.color + "''>" + this.points[1].series.name + '</span>: <b>' + this.points[1].y + '</b>';
                    p += "<br />"
                    //p += "<span style='color:" + this.points[1].series.color + "''>Gear Ratio</span>: <b>" + this.points[0].point.gearRatio + '</b>';
                    return p;
                }
            },
            series: [{
                name: 'Speed',
                type: 'spline',
                color: '#89A54E',
                data: speedArr,
                marker: {
                    enabled: false
                },
                dashStyle: 'shortdot',
                tooltip: {
                    valueSuffix: ' mph'
                }
            },
            {
                name: 'RPM',
                type: 'spline',
                color: '#AA4643',
                data: rpmArr,
                yAxis: 1,
                marker: {
                    enabled: false
                },
                dashStyle: 'shortdot',
                tooltip: {
                    valueSuffix: ' rpm'
                }
            }]
        });
    });
    