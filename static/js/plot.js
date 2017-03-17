/**
 * Created by yhu on 2017/2/8.
 */


 function error_mesage(indexValue) {
    $("#em_"+indexValue).show().html('<strong>Error:</strong> 需要选取两个');
 }


function plot_basis(chk_value, index) {
    $.getJSON("/basis/basis_json", {name1: chk_value[0], name2: chk_value[1]}, function (data) {
        var name_list = Object.keys(data["value"]);
        var myChart = echarts.init(document.getElementById(index), 'walden');
        var legend_list = name_list.slice();
        legend_list.push('diff');
        var option = {
            title: {
                text: index,
                x: 'center',
                align: 'right'
            },
            tooltip: {
                trigger: 'axis'
            },
            toolbox: {
                show: true,
                feature: {
                    dataZoom: {
                        yAxisIndex: 'none'
                    },
                    dataView: {readOnly: true},
                    restore: {},
                    saveAsImage: {}
                }
            },
            dataZoom: [
                {startValue: null},
                {type: 'inside'}
            ],
            legend: {
                data: legend_list,
                orient: 'vertical',
                right: 0,
                top: 'center'
            },
            xAxis: {
                name: '日期',
                type: 'category',
                data: data['date'],
                axisLabel: {
                    rotate: -20
                }
            },
            yAxis: [
                {
                    name: 'Price',
                    type: 'value',
                    scale: true
                },
                {
                    name: 'Diff',
                    type: 'value'
                }
            ],
            series: [
                {
                    name: name_list[0],
                    type: 'line',
                    data: data['value'][name_list[0]]
                },
                {
                    name: name_list[1],
                    type: 'line',
                    data: data['value'][name_list[1]]
                },
                {
                    name: 'diff',
                    type: 'line',
                    yAxisIndex: 1,
                    data: data['diff'],
                    markPoint: {
                        data: [
                            {type: 'max', name: '最大值'},
                            {type: 'min', name: '最小值'}
                        ]
                    }
                }
            ]
        };
        myChart.setOption(option);
    });
}


function getIndex(indexValue) {
    var chk_value =[];
    $('input[name=' + indexValue + ']:checked').each(function(){
        chk_value.push($(this).val());
    });
    $("#em_"+indexValue).hide().text('');
    if (chk_value.length!=2) {
        error_mesage(indexValue);
    }
    else {
        plot_basis(chk_value, indexValue);
    }
}


function plot_annualized(chk_value, index) {
    $.getJSON("/basis/basis_annualized_json", {name1: chk_value[0], name2: chk_value[1]}, function (data) {
        var myChart = echarts.init(document.getElementById(index), 'walden');
        var legend_list = ['annualized', 'basis'];
        var option = {
            title: {
                text: index,
                x: 'center',
                align: 'right'
            },
            tooltip: {
                trigger: 'axis',
                axisPointer: { // 坐标轴指示器，坐标轴触发有效
                    type: 'shadow' // 默认为直线，可选为：'line' | 'shadow | cross'
                }
            },
            toolbox: {
                show: true,
                feature: {
                    dataZoom: {
                        yAxisIndex: 'none'
                    },
                    dataView: {readOnly: true},
                    restore: {},
                    saveAsImage: {},
                    magicType: {
                        type: ['line']
                    }
                }
            },
            dataZoom: [
                {startValue: null},
                {type: 'inside'}
            ],
            legend: {
                data: legend_list,
                orient: 'vertical',
                right: 0,
                top: 'center'
            },
            xAxis: {
                name: '日期',
                type: 'category',
                data: data['date'],
                axisLabel: {
                    rotate: -20
                }
            },
            yAxis: [
                {
                    name: 'Basis',
                    type: 'value',
                    scale: true
                },
                {
                    name: 'Annualized %',
                    type: 'value',
                    scale: true
                }
            ],
            series: [
                {
                    name: 'annualized',
                    type: 'bar',
                    yAxisIndex: 1,
                    data: data['annualized'],
                    markPoint: {
                        data: [
                            {type: 'max', name: '最大值'},
                            {type: 'min', name: '最小值'}
                        ]
                    },
                    animationDelay: function (idx) {
                        return idx * 5;
                    },
                    animationDelayUpdate: function (idx) {
                        return idx * 5;
                    }
                },
                {
                    name: 'basis',
                    type: 'line',
                    data: data['basis']
                }
            ]
        };
        myChart.setOption(option);
    });
}


function getAnnualized(indexValue) {
    var chk_value =[];
    $('input[name=' + indexValue + ']:checked').each(function(){
        chk_value.push($(this).val());
    });
    $("#em_"+indexValue).hide().text('');
    if (chk_value.length!=2) {
        error_mesage(indexValue);
    }
    else {
        plot_annualized(chk_value, indexValue);
    }
}
