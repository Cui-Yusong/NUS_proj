import '../node_modules/@grapecity/wijmo.styles/wijmo.css';
import './styles.css';
import '../node_modules/bootstrap/dist/css/bootstrap.css';

import * as chart from '@grapecity/wijmo.chart';
import * as wjNav from '@grapecity/wijmo.nav';
//
document.readyState === 'complete' ? init() : window.onload = init;

function init() {
    new wjNav.TabPanel('#theTabPanel');

    // create the chart
    // console.log(getData())
    let theChart = new chart.FlexChart('#theChart', {
        itemsSource: getData(),
        bindingX: 'date',
        chartType: 'Candlestick',
        series: [
            {binding: 'high,low,open,close', name: 'Box Inc'}
        ],
        legend: {
            position: 'None'
        },
        tooltip: {
            content: '<b>{date:MMM dd}</b><br/>' +
                '<table>' +
                '<tr><td>high</td><td>{high:c}</td><tr/>' +
                '<tr><td>low</td><td>{low:c}</td><tr/>' +
                '<tr><td>open</td><td>{open:c}</td><tr/>' +
                '<tr><td>close</td><td>{close:c}</td><tr/>' +
                '</table>'
        }
    });


    let theChart1 = new chart.FlexChart('#theChart1', {
        itemsSource: getData(),
        bindingX: 'date',
        chartType: 'Candlestick',
        series: [
            {binding: 'high,low,open,close', name: 'Box Inc'}
        ],
        legend: {
            position: 'None'
        },
        tooltip: {
            content: '<b>{date:MMM dd}</b><br/>' +
                '<table>' +
                '<tr><td>high</td><td>{high:c}</td><tr/>' +
                '<tr><td>low</td><td>{low:c}</td><tr/>' +
                '<tr><td>open</td><td>{open:c}</td><tr/>' +
                '<tr><td>close</td><td>{close:c}</td><tr/>' +
                '</table>'
        }
    });


    let predChart = new chart.FlexChart('#predChart', {
        itemsSource: getData2(),
        bindingX: 'date',
        chartType: 'Candlestick',
        series: [
            {binding: 'high,low,open,close', name: 'Box Inc'}
        ],
        legend: {
            position: 'None'
        },
        tooltip: {
            content: '<b>{date:MMM dd}</b><br/>' +
                '<table>' +
                '<tr><td>high</td><td>{high:c}</td><tr/>' +
                '<tr><td>low</td><td>{low:c}</td><tr/>' +
                '<tr><td>open</td><td>{open:c}</td><tr/>' +
                '<tr><td>close</td><td>{close:c}</td><tr/>' +
                '</table>'
        }
    });

    theChart.palette = ['rgba(70,107,176,1)', 'rgba(200,180,34,1)', 'rgba(20,136,110,1)', 'rgba(181,72,54,1)',
        'rgba(110,89,68,1)', 'rgba(139,56,114,1)', 'rgba(115,178,43,1)', 'rgba(184,115,32,1)', 'rgba(20,20,20,1)'];
}


function getData2() {
    return [
        {date: new Date(2017, 1, 13), open: 816, high: 820.96, low: 815.49, close: 819.24, vol: 1213324},
        {date: new Date(2017, 1, 10), open: 811.7, high: 815.25, low: 809.78, close: 813.67, vol: 1134976},
        {date: new Date(2017, 1, 9), open: 809.51, high: 810.66, low: 804.54, close: 809.56, vol: 990391},
        {date: new Date(2017, 1, 8), open: 807, high: 811.84, low: 803.19, close: 808.38, vol: 1155990},
        {date: new Date(2017, 1, 7), open: 803.99, high: 810.5, low: 801.78, close: 806.97, vol: 1241221},
        {date: new Date(2017, 1, 6), open: 799.7, high: 801.67, low: 795.25, close: 801.34, vol: 1184483},
        {date: new Date(2017, 1, 3), open: 802.99, high: 806, low: 800.37, close: 801.49, vol: 1463448}
    ];
}


function getData() {
    var ans;
    $.ajaxSettings.async = false;
    $.getJSON("/getData", {}).done(
        function (rs) {
            // var back_data = rs["answer"];
            var back_data = rs;
            ans = [];
            for (var i = 0; i < back_data.length; i++) {
                var tmp = back_data[i];
                tmp["date"] = new Date(back_data[i]['date']);
                ans.push(tmp);
            }
        }
    )
    return ans;
}
