import * as wjcCore from '@grapecity/wijmo';
import { RequiredValidator, MinNumberValidator, MinDateValidator, MaxNumberValidator, MaxDateValidator } from './validation';
//
export class KeyValue {
}
KeyValue.NotFound = { key: -1, value: '' };
//
export class Country {
}
Country.NotFound = { id: -1, name: '', flag: '' };
//
export class DataService {
    constructor() {
        this._products = ['Widget', 'Gadget', 'Doohickey'];
        this._colors = ['Black', 'White', 'Red', 'Green', 'Blue'];
        this._countries = [
            { id: 0, name: 'US', flag: 'us' },
            { id: 1, name: 'Germany', flag: 'de' },
            { id: 2, name: 'UK', flag: 'gb' },
            { id: 3, name: 'Japan', flag: 'jp' },
            { id: 4, name: 'Italy', flag: 'it' },
            { id: 5, name: 'Greece', flag: 'gr' }
        ];
        this._validationConfig = {
            'date': [
                new RequiredValidator(),
                new MinDateValidator(new Date('2000-01-01T00:00:00')),
                new MaxDateValidator(new Date('2100-01-01T00:00:00'))
            ],
            'time': [
                new RequiredValidator(),
                new MinDateValidator(new Date('2000-01-01T00:00:00')),
                new MaxDateValidator(new Date('2100-01-01T00:00:00'))
            ],
            'productId': [
                new RequiredValidator(),
                new MinNumberValidator(0, `{0} can't be less than {1} (${this._products[0]})`),
                new MaxNumberValidator(this._products.length - 1, `{0} can't be greater than {1} (${this._products[this._products.length - 1]})`)
            ],
            'countryId': [
                new RequiredValidator(),
                new MinNumberValidator(0, `{0} can't be less than {1} (${this._countries[0].name})`),
                new MaxNumberValidator(this._countries.length - 1, `{0} can't be greater than {1} (${this._countries[this._countries.length - 1].name})`)
            ],
            'colorId': [
                new RequiredValidator(),
                new MinNumberValidator(0, `{0} can't be less than {1} (${this._colors[0]})`),
                new MaxNumberValidator(this._colors.length - 1, `{0} can't be greater than {1} (${this._colors[this._colors.length - 1]})`)
            ],
            'price': [
                new RequiredValidator(),
                new MinNumberValidator(0, `Price can't be a negative value`)
            ]
        };
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
        const data = [];
        const dt = new Date();
        const year = dt.getFullYear();
        const itemsCount = Math.max(count, 5);
        // add items
        for (let i = 0; i < itemsCount; i++) {
            const item = this._getItem(i, year);
            data.push(item);
        }
        // set invalid data to demonstrate errors visualization
        data[1].price = -2000;
        data[2].date = new Date('1970-01-01T00:00:00');
        data[4].time = undefined;
        data[4].price = -1000;
        return data;
    }
    validate(item, prop, displayName) {
        const validators = this._validationConfig[prop];
        if (wjcCore.isUndefined(validators)) {
            return '';
        }
        const value = item[prop];
        for (let i = 0; i < validators.length; i++) {
            const validationError = validators[i].validate(displayName, value);
            if (!wjcCore.isNullOrWhiteSpace(validationError)) {
                return validationError;
            }
        }
    }
    _getItem(i, year) {
        const date = new Date(year, i % 12, 25, i % 24, i % 60, i % 60);
        const countryIndex = this._getRandomIndex(this._countries);
        const productIndex = this._getRandomIndex(this._products);
        const colorIndex = this._getRandomIndex(this._colors);
        const item = {
            id: i,
            date: date,
            time: new Date(date.getTime() + Math.random() * 30 * (24 * 60 * 60 * 1000)),
            countryId: this._countries[countryIndex].id,
            productId: productIndex,
            colorId: colorIndex,
            price: wjcCore.toFixed(Math.random() * 10000 + 5000, 2, true),
            change: wjcCore.toFixed(Math.random() * 1000 - 500, 2, true),
            history: this.getHistoryData(),
            discount: wjcCore.toFixed(Math.random() / 4, 2, true),
            rating: this._getRating(),
            active: i % 4 == 0,
            size: Math.floor(100 + Math.random() * 900),
            weight: Math.floor(100 + Math.random() * 900),
            quantity: Math.floor(Math.random() * 10),
            description: "Across all our software products and services, our focus is on helping our customers achieve their goals. Our key principles – thoroughly understanding our customers' business objectives, maintaining a strong emphasis on quality, and adhering to the highest ethical standards – serve as the foundation for everything we do."
        };
        return item;
    }
    _getRating() {
        return Math.ceil(Math.random() * 5);
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
