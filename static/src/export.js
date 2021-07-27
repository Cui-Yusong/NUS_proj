import * as wjcCore from '@grapecity/wijmo';
import * as wjcGrid from '@grapecity/wijmo.grid';
import * as wjcGridPdf from '@grapecity/wijmo.grid.pdf';
import * as wjcGridXlsx from '@grapecity/wijmo.grid.xlsx';
import * as wjcPdf from '@grapecity/wijmo.pdf';
import * as wjcXlsx from '@grapecity/wijmo.xlsx';
import { KeyValue, Country } from './data';
//
const ExcelExportDocName = 'FlexGrid.xlsx';
const PdfExportDocName = 'FlexGrid.pdf';
const FakeColumn = new wjcGrid.Column();
const FakeRow = new wjcGrid.Row();
//
class Fonts {
}
Fonts.ZapfDingbatsSm = new wjcPdf.PdfFont('zapfdingbats', 8, 'normal', 'normal');
Fonts.ZapfDingbatsLg = new wjcPdf.PdfFont('zapfdingbats', 16, 'normal', 'normal');
//
export class IExcelExportContext {
}
//
export class ExportService {
    startExcelExport(flex, ctx) {
        if (ctx.preparing || ctx.exporting) {
            return;
        }
        ctx.exporting = false;
        ctx.progress = 0;
        ctx.preparing = true;
        wjcGridXlsx.FlexGridXlsxConverter.saveAsync(flex, {
            includeColumnHeaders: true,
            includeCellStyles: false,
            formatItem: this._formatExcelItem.bind(this)
        }, ExcelExportDocName, () => {
            console.log('Export to Excel completed');
            this._resetExcelContext(ctx);
        }, err => {
            console.error(`Export to Excel failed: ${err}`);
            this._resetExcelContext(ctx);
        }, prg => {
            if (ctx.preparing) {
                ctx.exporting = true;
                ctx.preparing = false;
            }
            ctx.progress = prg / 100.;
        }, true);
        console.log('Export to Excel started');
    }
    cancelExcelExport(ctx) {
        wjcGridXlsx.FlexGridXlsxConverter.cancelAsync(() => {
            console.log('Export to Excel canceled');
            this._resetExcelContext(ctx);
        });
    }
    exportToPdf(flex, options) {
        wjcGridPdf.FlexGridPdfConverter.export(flex, PdfExportDocName, {
            maxPages: 100,
            exportMode: wjcGridPdf.ExportMode.All,
            scaleMode: wjcGridPdf.ScaleMode.ActualSize,
            documentOptions: {
                pageSettings: {
                    layout: wjcPdf.PdfPageOrientation.Landscape
                },
                header: {
                    declarative: {
                        text: '\t&[Page]\\&[Pages]'
                    }
                },
                footer: {
                    declarative: {
                        text: '\t&[Page]\\&[Pages]'
                    }
                }
            },
            styles: {
                cellStyle: {
                    backgroundColor: '#ffffff',
                    borderColor: '#c6c6c6'
                },
                altCellStyle: {
                    backgroundColor: '#f9f9f9'
                },
                groupCellStyle: {
                    backgroundColor: '#dddddd'
                },
                headerCellStyle: {
                    backgroundColor: '#eaeaea'
                },
                // Highlight Invalid Cells
                errorCellStyle: {
                    backgroundColor: 'rgba(255, 0, 0, 0.3)'
                }
            },
            customCellContent: false,
            formatItem: (e) => this._formatPdfItem(e, options)
        });
    }
    _formatExcelItem(e) {
        const panel = e.panel;
        if (panel.cellType !== wjcGrid.CellType.Cell) {
            return;
        }
        // highlight invalid cells
        if (panel.grid._getError(panel, e.row, e.col)) {
            const fill = new wjcXlsx.WorkbookFill();
            fill.color = '#ff0000';
            e.xlsxCell.style.fill = fill;
        }
    }
    _resetExcelContext(ctx) {
        ctx.exporting = false;
        ctx.progress = 0;
        ctx.preparing = false;
    }
    _formatPdfItem(e, options) {
        const panel = e.panel;
        if (panel.cellType !== wjcGrid.CellType.Cell) {
            return;
        }
        switch (panel.columns[e.col].binding) {
            case 'countryId':
                this._formatPdfCountryCell(e, options.countryMap);
                break;
            case 'colorId':
                this._formatPdfColorCell(e, options.colorMap);
                break;
            case 'change':
                this._formatPdfChangeCell(e);
                break;
            case 'history':
                /*** Version #1: get grid cell produced before by a cell template ***/
                // const cell = e.getFormattedCell();
                // this._formatPdfHistoryCell(e, cell);
                /*** Version #2: create fake cell from a cell template ***/
                const history = e.panel.getCellData(e.row, e.col, false);
                const cell = this._createCellFromCellTemplate(options.historyCellTemplate, history);
                this._formatPdfHistoryCell(e, cell);
                break;
            case 'rating':
                this._formatPdfRatingCell(e);
                break;
        }
    }
    _formatPdfCountryCell(e, countryMap) {
        e.drawBackground(e.style.backgroundColor);
        // check whether country exists
        const countryName = e.data;
        if (this._isCountryExist(countryName, countryMap)) {
            // bound rectangle of cell's content area
            const contentRect = e.contentRect;
            // draw flag image
            const image = e.canvas.openImage(`resources/${countryName}.png`);
            const imageTop = contentRect.top + (contentRect.height - image.height) / 2;
            e.canvas.drawImage(image, contentRect.left, imageTop);
            // draw country name
            e.canvas.drawText(countryName, contentRect.left + image.width + 3, e.textTop);
        }
        // cancel standard cell content drawing
        e.cancel = true;
    }
    _formatPdfColorCell(e, colorMap) {
        e.drawBackground(e.style.backgroundColor);
        // check whether color exists
        const colorName = e.data;
        if (this._isColorExist(colorName, colorMap)) {
            // bound rectangle of cell's content area
            const contentRect = e.contentRect;
            // draw color indicator
            const imageHeight = Math.min(10, contentRect.height);
            const imageWidth = 1.33 * imageHeight;
            const imageTop = contentRect.top + (contentRect.height - imageHeight) / 2;
            e.canvas.paths
                .rect(contentRect.left, imageTop, imageWidth, imageHeight)
                .fillAndStroke(wjcCore.Color.fromString(colorName), wjcCore.Color.fromString('gray'));
            // draw color name
            e.canvas.drawText(colorName, contentRect.left + imageWidth + 3, e.textTop);
        }
        // cancel standard cell content drawing
        e.cancel = true;
    }
    _formatPdfChangeCell(e) {
        e.drawBackground(e.style.backgroundColor);
        // get change value and text
        const cellData = e.panel.getCellData(e.row, e.col, false);
        let change = 0;
        let changeText = '';
        if (wjcCore.isNumber(cellData)) {
            change = cellData;
            changeText = wjcCore.Globalize.formatNumber(change, 'c');
        }
        else if (!wjcCore.isUndefined(cellData) && cellData !== null) {
            changeText = wjcCore.changeType(cellData, wjcCore.DataType.String);
        }
        // determine whether change is positive or negative
        let changeIndicator = '';
        let changeColor = e.style.color;
        if (change > 0) {
            changeIndicator = '\x73'; // ▲
            changeColor = 'darkgreen';
        }
        else if (change < 0) {
            changeIndicator = '\x74'; // ▼
            changeColor = 'darkred';
        }
        // draw change indicator
        let indent = 10;
        e.canvas.drawText(changeIndicator, e.contentRect.right - indent, e.contentRect.top + indent, {
            brush: changeColor,
            font: Fonts.ZapfDingbatsSm
        });
        // draw change text
        indent += 3;
        e.canvas.drawText(changeText, e.contentRect.left, e.textTop, {
            brush: changeColor,
            align: wjcPdf.PdfTextHorizontalAlign.Right,
            width: e.contentRect.width - indent
        });
        // cancel standard cell content drawing
        e.cancel = true;
    }
    _formatPdfHistoryCell(e, cell) {
        e.drawBackground(e.style.backgroundColor);
        // draw history svg
        const svgUrl = this._getHistorySvgDataUrlFromCell(cell, e.clientRect.width, e.clientRect.height);
        if (svgUrl) {
            let cr = e.contentRect;
            e.canvas.drawSvg(svgUrl, cr.left + 2, cr.top + 2, { width: cr.width - 4, height: cr.height - 4 });
        }
        // cancel standard cell content drawing
        e.cancel = true;
    }
    _getHistorySvgDataUrlFromCell(cell, width, height) {
        let dataUrl = null;
        // extract SVG from provided cell
        const svg = cell.getElementsByTagName('svg')[0];
        if (svg) {
            const clone = svg.cloneNode(true);
            clone.setAttribute('version', '1.1');
            clone.setAttributeNS('http://www.w3.org/2000/xmlns/', 'xmlns', 'http://www.w3.org/2000/svg');
            clone.style.overflow = 'visible';
            clone.style.stroke = '#376092';
            clone.style.fill = '#376092';
            const s = document.createElement('style');
            s.setAttribute('type', 'text/css');
            s.innerHTML = `<![CDATA[
          line { 
              stroke-width: 2;
          }
          circle { 
              stroke-width: 0;
              stroke-opacity: 0; 
          }
          .wj-marker { 
              fill: #d00000; 
              opacity: 1; 
          }
      ]]>`;
            const defs = document.createElement('defs');
            defs.appendChild(s);
            clone.insertBefore(defs, clone.firstChild);
            const outer = document.createElement('div');
            outer.appendChild(clone);
            dataUrl = 'data:image/svg+xml;base64,' + btoa(unescape(encodeURIComponent(outer.innerHTML)));
        }
        return dataUrl;
    }
    _formatPdfRatingCell(e) {
        e.drawBackground(e.style.backgroundColor);
        // check whether rating is defined
        let rating = wjcCore.changeType(e.data, wjcCore.DataType.Number);
        if (wjcCore.isInt(rating)) {
            const ratingIndicator = '\x48'; // ★
            const ratingNormalColor = wjcCore.Color.fromRgba(255, 165, 0, 1); // orange
            const ratingLightColor = wjcCore.Color.fromRgba(255, 165, 0, 0.2);
            // draw rating indicators
            const indent = 16;
            const count = 5;
            const width = count * indent;
            const y = e.clientRect.top + indent;
            let x = e.contentRect.left + (e.contentRect.width - width) / 2;
            rating = wjcCore.clamp(rating, 1, count);
            for (let i = 0; i < count; i++) {
                e.canvas.drawText(ratingIndicator, x, y, {
                    brush: (i < rating) ? ratingNormalColor : ratingLightColor,
                    font: Fonts.ZapfDingbatsLg,
                    height: e.clientRect.height
                });
                x += indent;
            }
        }
        // cancel standard cell content drawing
        e.cancel = true;
    }
    _isCountryExist(countryName, countryMap) {
        const countryId = countryMap.getKeyValue(countryName);
        if (wjcCore.isUndefined(countryId) || countryId === null) {
            return false;
        }
        if (countryId === Country.NotFound.id) {
            return false;
        }
        return true;
    }
    _isColorExist(colorName, colorMap) {
        const colorId = colorMap.getKeyValue(colorName);
        if (wjcCore.isUndefined(colorId) || colorId === null) {
            return false;
        }
        if (colorId === KeyValue.NotFound.key) {
            return false;
        }
        return true;
    }
    _createCellFromCellTemplate(cellTemplate, data) {
        const cell = document.createElement('div');
        cellTemplate({
            col: FakeColumn,
            row: FakeRow,
            value: data,
            item: null,
            text: null
        }, cell);
        return cell;
    }
}
