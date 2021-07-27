import * as wjcCore from '@grapecity/wijmo';
import {
    RequiredValidator,
    MinNumberValidator,
    MinDateValidator,
    MaxNumberValidator,
    MaxDateValidator
} from './validation';

//
export class KeyValue {
}

KeyValue.NotFound = {key: -1, value: ''};

//
export class Country {
}

Country.NotFound = {id: -1, name: '', flag: ''};

//
export class DataService {
    constructor() {
        this._products = ['Widget', 'Gadget', 'Doohickey'];
        this._colors = ['Black', 'White', 'Red', 'Green', 'Blue'];
        this._countries = [
            {id: 0, name: '人民币', flag: 'us'}
            // { id: 1, name: 'Germany', flag: 'de' },
            // { id: 2, name: 'UK', flag: 'gb' },
            // { id: 3, name: 'Japan', flag: 'jp' },
            // { id: 4, name: 'Italy', flag: 'it' },
            // { id: 5, name: 'Greece', flag: 'gr' }
        ];
        // this._validationConfig = {
        //     'date': [
        //         new RequiredValidator(),
        //         new MinDateValidator(new Date('2000-01-01T00:00:00')),
        //         new MaxDateValidator(new Date('2100-01-01T00:00:00'))
        //     ],
        //     'time': [
        //         new RequiredValidator(),
        //         new MinDateValidator(new Date('2000-01-01T00:00:00')),
        //         new MaxDateValidator(new Date('2100-01-01T00:00:00'))
        //     ],
        //     'productId': [
        //         new RequiredValidator(),
        //         new MinNumberValidator(0, `{0} can't be less than {1} (${this._products[0]})`),
        //         new MaxNumberValidator(this._products.length - 1, `{0} can't be greater than {1} (${this._products[this._products.length - 1]})`)
        //     ],
        //     'countryId': [
        //         new RequiredValidator(),
        //         new MinNumberValidator(0, `{0} can't be less than {1} (${this._countries[0].name})`),
        //         new MaxNumberValidator(this._countries.length - 1, `{0} can't be greater than {1} (${this._countries[this._countries.length - 1].name})`)
        //     ],
        //     'colorId': [
        //         new RequiredValidator(),
        //         new MinNumberValidator(0, `{0} can't be less than {1} (${this._colors[0]})`),
        //         new MaxNumberValidator(this._colors.length - 1, `{0} can't be greater than {1} (${this._colors[this._colors.length - 1]})`)
        //     ]
        // };
    }

    getCountries() {
        return this._countries;
    }

    getProducts() {
        return this._products;
    }

    getColors() {
        return this._colors;
    }

    getHistoryData() {
        return this._getRandomArray(25, 100);
    }

    getData(count) {
        var data = [];
        $.ajaxSettings.async = false;
        $.getJSON("/getData_grid", {}).done(
            function (rs) {
                console.log(rs)
                for (var i = 0; i < 500; i++) {
                    data.push(rs[i])
                }
                console.log(data)
            }
        )
        return data;

    }

    // getData2(count) {
    //     const data = [];
    //     const dt = new Date();
    //     const year = dt.getFullYear();
    //     const itemsCount = Math.max(count, 5);
    //     // add items
    //     for (let i = 0; i < itemsCount; i++) {
    //         const item = this._getItem(i, year);
    //         data.push(item);
    //     }
    //     console.log(data)
    //
    //     return data;
    // }

    _getItem(i, year) {
        const item = {
            code: i,
            name: 'name',
            open: 500,
            close: 400,
            high: 300,
            low: 200,
            amount: 100,
            change: 'temp',
            history: this.getHistoryData(),
            rating: Math.ceil((i) % 6),
        };
        return item;
    }

    _getRandomIndex(arr) {
        return Math.floor(Math.random() * arr.length);
    }

    _getRandomArray(len, maxValue) {
        const arr = [];
        for (let i = 0; i < len; i++) {
            arr.push(Math.floor(Math.random() * maxValue));
        }
        return arr;
    }
}
