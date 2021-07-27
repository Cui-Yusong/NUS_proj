import 'bootstrap.css';
import '@grapecity/wijmo.styles/wijmo.css';
import './styles.css';
//
import '@grapecity/wijmo.touch';
import * as wjcCore from '@grapecity/wijmo';
import * as wjcGrid from '@grapecity/wijmo.grid';
import * as wjcGridFilter from '@grapecity/wijmo.grid.filter';
import * as wjcGridSearch from '@grapecity/wijmo.grid.search';
import * as wjcGridGroupPanel from '@grapecity/wijmo.grid.grouppanel';
import * as wjcInput from '@grapecity/wijmo.input';
import { CellMaker, SparklineMarkers } from '@grapecity/wijmo.grid.cellmaker';
import { KeyValue, Country, DataService } from './data';
import { ExportService } from './export';
//
class App {
    constructor(dataSvc) {
        this._itemsCount = 500;
        this._lastId = this._itemsCount;
        this._dataSvc = dataSvc;
        // initializes data maps
        // this._productMap = this._buildDataMap(this._dataSvc.getProducts());
        this._countryMap = new wjcGrid.DataMap(this._dataSvc.getCountries(), 'id', 'name');
        // this._colorMap = this._buildDataMap(this._dataSvc.getColors());
        // initializes cell templates
        this._historyCellTemplate = CellMaker.makeSparkline({
            markers: SparklineMarkers.High | SparklineMarkers.Low,
            maxPoints: 25,
            label: 'price history',
        });
        this._ratingCellTemplate = CellMaker.makeRating({
            range: [1, 5],
            label: 'rating'
        });
        // initializes data size
        // document.getElementById('itemsCount').addEventListener('change', (e) => {
        //     const value = e.target.value;
        //     this._itemsCount = wjcCore.changeType(value, wjcCore.DataType.Number);
        //     this._handleItemsCountChange();
        // });
        // // initializes export
        // const btnExportToExcel = document.getElementById('btnExportToExcel');
        // this._excelExportContext = new ExcelExportContext(btnExportToExcel);
        // btnExportToExcel.addEventListener('click', () => {
        //     this._exportToExcel();
        // });
        // document.getElementById('btnExportToPdf').addEventListener('click', () => {
        //     this._exportToPdf();
        // });
        // initializes the grid
        this._initializeGrid();
        // initializes items source
        this._itemsSource = this._createItemsSource();
        this._theGrid.itemsSource = this._itemsSource;
    }
    close() {
        const ctx = this._excelExportContext;
        this._exportSvc.cancelExcelExport(ctx);
    }
    _initializeGrid() {
        // creates the grid
        this._theGrid = new wjcGrid.FlexGrid('#theGrid', {
            autoGenerateColumns: false,
            allowAddNew: true,
            allowDelete: true,
            allowPinning: wjcGrid.AllowPinning.SingleColumn,
            newRowAtTop: true,
            showMarquee: true,
            selectionMode: wjcGrid.SelectionMode.MultiRange,
            validateEdits: false,
            columns: [
                { binding: 'id', header: 'Code', width: 100, isReadOnly: true },
                // {
                //     binding: 'date', header: 'Date', format: 'MMM d yyyy', isRequired: false, width: 130,
                //     editor: new wjcInput.InputDate(document.createElement('div'), {
                //         format: 'MM/dd/yyyy',
                //         isRequired: false
                //     })
                // },
                {
                    binding: 'countryId', header: 'Name', dataMap: this._countryMap, width: 145,
                    cellTemplate: (ctx) => {
                        const dataItem = ctx.row.dataItem;
                        if (wjcCore.isUndefined(dataItem) || dataItem === null) {
                            return '';
                        }
                        const country = '￥人民';
                        return `${country}`;
                    }
                },
                { binding: 'price', header: 'Open', isRequired: false, width: 100 },
                { binding: 'price', header: 'Close', format: 'c', isRequired: false, width: 100 },

                { binding: 'price', header: 'High', format: 'c', isRequired: false, width: 100 },

                { binding: 'price', header: 'Low', format: 'c', isRequired: false, width: 100 },
                { binding: 'price', header: 'Amount', format: 'c', isRequired: false, width: 150 },

                {
                    binding: 'history', header: 'History', width: 180, align: 'center', allowSorting: false,
                    cellTemplate: this._historyCellTemplate
                },
                {
                    binding: 'rating', header: 'Rating', width: 180, align: 'center', cssClass: 'cell-rating',
                    cellTemplate: this._ratingCellTemplate
                }
                // ,
                // {
                //     binding: 'time', header: 'Time', format: 'HH:mm', isRequired: false, width: 95,
                //     editor: new wjcInput.InputTime(document.createElement('div'), {
                //         format: 'HH:mm',
                //         isRequired: false
                //     })
                // },
                // {
                //     binding: 'colorId', header: 'Volume', dataMap: this._colorMap, width: 145,
                //     cellTemplate: (ctx) => {
                //         const dataItem = ctx.row.dataItem;
                //         if (wjcCore.isUndefined(dataItem) || dataItem === null) {
                //             return '';
                //         }
                //         const color = this._getColor(ctx.item);
                //         return `<span class="color-tile" style="background: ${color.value}"></span> ${color.value}`;
                //     }
                // },
                // { binding: 'productId', header: 'Product', dataMap: this._productMap, width: 145 },
                // { binding: 'discount', header: 'Discount', format: 'p0', width: 130 },
                // { binding: 'active', header: 'Active', width: 100 }
            ]
        });
        // create the grid search box
        // new wjcGridSearch.FlexGridSearch('#theSearch', {
        //     placeholder: 'Search',
        //     grid: this._theGrid,
        //     cssMatch: ''
        // });
        // // adds Excel-like filter
        // new wjcGridFilter.FlexGridFilter(this._theGrid, {
        //     filterColumns: [
        //         'id', 'date', 'time', 'countryId', 'productId',
        //         'colorId', 'price', 'change', 'discount', 'rating', 'active'
        //     ]
        // });
        // // adds group panel
        // new wjcGridGroupPanel.GroupPanel('#theGroupPanel', {
        //     placeholder: 'Drag columns here to create groups',
        //     grid: this._theGrid
        // });
    }
    _getCountry(item) {
        const country = this._countryMap.getDataItem(item.countryId);
        return country ? country : Country.NotFound;
    }
    _getColor(item) {
        const color = this._colorMap.getDataItem(item.colorId);
        return color ? color : KeyValue.NotFound;
    }
    _getChangeCls(value) {
        if (wjcCore.isNumber(value)) {
            if (value > 0) {
                return 'change-up';
            }
            if (value < 0) {
                return 'change-down';
            }
        }
        return '';
    }
    _formatChange(value) {
        if (wjcCore.isNumber(value)) {
            return wjcCore.Globalize.formatNumber(value, 'c');
        }
        if (!wjcCore.isUndefined(value) && value !== null) {
            return wjcCore.changeType(value, wjcCore.DataType.String);
        }
        return '';
    }
    _exportToExcel() {
        const ctx = this._excelExportContext;
        if (!ctx.exporting) {
            this._exportSvc.startExcelExport(this._theGrid, ctx);
        }
        else {
            this._exportSvc.cancelExcelExport(ctx);
        }
    }
    _exportToPdf() {
        this._exportSvc.exportToPdf(this._theGrid, {
            countryMap: this._countryMap,
            colorMap: this._colorMap,
            historyCellTemplate: this._historyCellTemplate
        });
    }
    _createItemsSource() {
        const data = this._dataSvc.getData(this._itemsCount);
        const view = new wjcCore.CollectionView(data, {
            getError: (item, prop) => {
                const displayName = this._theGrid.columns.getColumn(prop).header;
                return false;
            }
        });
        view.collectionChanged.addHandler((s, e) => {
            // initializes new added item with a history data
            if (e.action === wjcCore.NotifyCollectionChangedAction.Add) {
                e.item.history = this._dataSvc.getHistoryData();
                e.item.id = this._lastId;
                this._lastId++;
            }
        });
        return view;
    }
    _disposeItemsSource(itemsSource) {
        if (itemsSource) {
            itemsSource.collectionChanged.removeAllHandlers();
        }
    }
    // build a data map from a string array using the indices as keys
    _buildDataMap(items) {
        const map = [];
        for (let i = 0; i < items.length; i++) {
            map.push({ key: i, value: items[i] });
        }
        return new wjcGrid.DataMap(map, 'key', 'value');
    }
    _handleItemsCountChange() {
        this._disposeItemsSource(this._itemsSource);
        this._lastId = this._itemsCount;
        this._itemsSource = this._createItemsSource();
        this._theGrid.itemsSource = this._itemsSource;
    }
}
//
class ExcelExportContext {
    constructor(btn) {
        this._exporting = false;
        this._progress = 0;
        this._preparing = false;
        this._btn = btn;
    }
    get exporting() {
        return this._exporting;
    }
    set exporting(value) {
        if (value !== this._exporting) {
            this._exporting = value;
            this._onPropertyChanged();
        }
    }
    get progress() {
        return this._progress;
    }
    set progress(value) {
        if (value !== this._progress) {
            this._progress = value;
            this._onPropertyChanged();
        }
    }
    get preparing() {
        return this._preparing;
    }
    set preparing(value) {
        if (value !== this._preparing) {
            this._preparing = value;
            this._onPropertyChanged();
        }
    }
    _onPropertyChanged() {
        wjcCore.enable(this._btn, !this._preparing);
        if (this._exporting) {
            const percent = wjcCore.Globalize.formatNumber(this._progress, 'p0');
            this._btn.textContent = `Cancel (${percent} done)`;
        }
        else {
            this._btn.textContent = 'Export To Excel';
        }
    }
}
//
document.readyState === 'complete' ? init() : window.onload = init;
//
function init() {
    const dataSvc = new DataService();
    // const exportSvc = new ExportService();
    const app = new App(dataSvc);
    window.addEventListener('unload', () => {
        app.close();
    });
}
