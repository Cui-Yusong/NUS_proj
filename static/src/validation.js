import * as wjcCore from '@grapecity/wijmo';
export class RequiredValidator {
    validate(name, value) {
        const message = name + ' is required';
        if (wjcCore.isUndefined(value)) {
            return message;
        }
        const str = wjcCore.changeType(value, wjcCore.DataType.String);
        if (wjcCore.isNullOrWhiteSpace(str)) {
            return message;
        }
        return '';
    }
}
export class MinValueValidator {
    constructor(minValue, message = '{0} can\'t be less than {1}', format = null) {
        this.minValue = minValue;
        this.message = message;
        this.format = format;
    }
    validate(name, value) {
        if (value < this.minValue) {
            return wjcCore.format(this.message, {
                0: name,
                1: this._formatValue(this.minValue)
            });
        }
        return '';
    }
}
export class MaxValueValidator {
    constructor(maxValue, message = '{0} can\'t be greater than {1}', format = null) {
        this.maxValue = maxValue;
        this.message = message;
        this.format = format;
    }
    validate(name, value) {
        if (value > this.maxValue) {
            return wjcCore.format(this.message, {
                0: name,
                1: this._formatValue(this.maxValue)
            });
        }
        return '';
    }
}
export class MinNumberValidator extends MinValueValidator {
    constructor(minValue, message = '{0} can\'t be less than {1}', format = 'n') {
        super(minValue, message, format);
    }
    _formatValue(value) {
        return wjcCore.Globalize.formatNumber(value, this.format);
    }
}
export class MaxNumberValidator extends MaxValueValidator {
    constructor(maxValue, message = '{0} can\'t be greater than {1}', format = 'n') {
        super(maxValue, message, format);
    }
    _formatValue(value) {
        return wjcCore.Globalize.formatNumber(value, this.format);
    }
}
export class MinDateValidator extends MinValueValidator {
    constructor(minValue, message = '{0} can\'t be less than {1}', format = 'MM/dd/yyyy') {
        super(minValue, message, format);
    }
    _formatValue(value) {
        return wjcCore.Globalize.formatDate(value, this.format);
    }
}
export class MaxDateValidator extends MaxValueValidator {
    constructor(maxValue, message = '{0} can\'t be greater than {1}', format = 'MM/dd/yyyy') {
        super(maxValue, message, format);
    }
    _formatValue(value) {
        return wjcCore.Globalize.formatDate(value, this.format);
    }
}
