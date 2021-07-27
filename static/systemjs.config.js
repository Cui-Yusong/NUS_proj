(function (global) {
    System.config({
        transpiler: 'plugin-babel',
        babelOptions: {
            es2015: true
        },
        meta: {
            '*.css': { loader: 'css' }
        },
        paths: {
            // paths serve as alias
            'npm:': 'node_modules/'
        },
        // map tells the System loader where to look for things
        map: {
            'jszip': 'npm:jszip/dist/jszip.js',
            '@grapecity/wijmo': 'npm:@grapecity/wijmo/index.js',
            '@grapecity/wijmo.input': 'npm:@grapecity/wijmo.input/index.js',
            '@grapecity/wijmo.styles': 'npm:@grapecity/wijmo.styles',
            '@grapecity/wijmo.cultures': 'npm:@grapecity/wijmo.cultures',
            '@grapecity/wijmo.chart': 'npm:@grapecity/wijmo.chart/index.js',
            '@grapecity/wijmo.chart.analytics': 'npm:@grapecity/wijmo.chart.analytics/index.js',
            '@grapecity/wijmo.chart.animation': 'npm:@grapecity/wijmo.chart.animation/index.js',
            '@grapecity/wijmo.chart.annotation': 'npm:@grapecity/wijmo.chart.annotation/index.js',
            '@grapecity/wijmo.chart.finance': 'npm:@grapecity/wijmo.chart.finance/index.js',
            '@grapecity/wijmo.chart.finance.analytics': 'npm:@grapecity/wijmo.chart.finance.analytics/index.js',
            '@grapecity/wijmo.chart.hierarchical': 'npm:@grapecity/wijmo.chart.hierarchical/index.js',
            '@grapecity/wijmo.chart.interaction': 'npm:@grapecity/wijmo.chart.interaction/index.js',
            '@grapecity/wijmo.chart.radar': 'npm:@grapecity/wijmo.chart.radar/index.js',
            '@grapecity/wijmo.chart.render': 'npm:@grapecity/wijmo.chart.render/index.js',
            '@grapecity/wijmo.chart.webgl': 'npm:@grapecity/wijmo.chart.webgl/index.js',
            '@grapecity/wijmo.chart.map': 'npm:@grapecity/wijmo.chart.map/index.js',
            '@grapecity/wijmo.gauge': 'npm:@grapecity/wijmo.gauge/index.js',
            '@grapecity/wijmo.grid': 'npm:@grapecity/wijmo.grid/index.js',
            '@grapecity/wijmo.grid.detail': 'npm:@grapecity/wijmo.grid.detail/index.js',
            '@grapecity/wijmo.grid.filter': 'npm:@grapecity/wijmo.grid.filter/index.js',
            '@grapecity/wijmo.grid.search': 'npm:@grapecity/wijmo.grid.search/index.js',
            '@grapecity/wijmo.grid.grouppanel': 'npm:@grapecity/wijmo.grid.grouppanel/index.js',
            '@grapecity/wijmo.grid.multirow': 'npm:@grapecity/wijmo.grid.multirow/index.js',
            '@grapecity/wijmo.grid.transposed': 'npm:@grapecity/wijmo.grid.transposed/index.js',
            '@grapecity/wijmo.grid.transposedmultirow': 'npm:@grapecity/wijmo.grid.transposedmultirow/index.js',
            '@grapecity/wijmo.grid.pdf': 'npm:@grapecity/wijmo.grid.pdf/index.js',
            '@grapecity/wijmo.grid.sheet': 'npm:@grapecity/wijmo.grid.sheet/index.js',
            '@grapecity/wijmo.grid.xlsx': 'npm:@grapecity/wijmo.grid.xlsx/index.js',
            '@grapecity/wijmo.grid.selector': 'npm:@grapecity/wijmo.grid.selector/index.js',
            '@grapecity/wijmo.grid.cellmaker': 'npm:@grapecity/wijmo.grid.cellmaker/index.js',
            '@grapecity/wijmo.nav': 'npm:@grapecity/wijmo.nav/index.js',
            '@grapecity/wijmo.odata': 'npm:@grapecity/wijmo.odata/index.js',
            '@grapecity/wijmo.olap': 'npm:@grapecity/wijmo.olap/index.js',
            '@grapecity/wijmo.rest': 'npm:@grapecity/wijmo.rest/index.js',
            '@grapecity/wijmo.pdf': 'npm:@grapecity/wijmo.pdf/index.js',
            '@grapecity/wijmo.pdf.security': 'npm:@grapecity/wijmo.pdf.security/index.js',
            '@grapecity/wijmo.viewer': 'npm:@grapecity/wijmo.viewer/index.js',
            '@grapecity/wijmo.xlsx': 'npm:@grapecity/wijmo.xlsx/index.js',
            '@grapecity/wijmo.undo': 'npm:@grapecity/wijmo.undo/index.js',
            '@grapecity/wijmo.interop.grid': 'npm:@grapecity/wijmo.interop.grid/index.js',
            '@grapecity/wijmo.touch': 'npm:@grapecity/wijmo.touch/index.js',
            '@grapecity/wijmo.cloud': 'npm:@grapecity/wijmo.cloud/index.js',
            '@grapecity/wijmo.barcode': 'npm:@grapecity/wijmo.barcode/index.js',
            '@grapecity/wijmo.barcode.common': 'npm:@grapecity/wijmo.barcode.common/index.js',
            '@grapecity/wijmo.barcode.composite': 'npm:@grapecity/wijmo.barcode.composite/index.js',
            '@grapecity/wijmo.barcode.specialized': 'npm:@grapecity/wijmo.barcode.specialized/index.js',
            'jszip': 'npm:jszip/dist/jszip.js',
            'bootstrap.css': 'npm:bootstrap/dist/css/bootstrap.min.css',
            'css': 'npm:systemjs-plugin-css/css.js',
            'plugin-babel': 'npm:systemjs-plugin-babel/plugin-babel.js',
            'systemjs-babel-build':'npm:systemjs-plugin-babel/systemjs-babel-browser.js'
        },
        // packages tells the System loader how to load when no filename and/or no extension
        packages: {
            src: {
                defaultExtension: 'js'
            },
            "node_modules": {
                defaultExtension: 'js'
            },
        }
    });
})(this);
