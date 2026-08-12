class ROICalculator {
  constructor(template) {
    this.template = template;
    this.parser = new ExpressionParser(); // math.js or similar
  }
  
  calculate(inputs) {
    const results = {};
    const context = { ...inputs };
    
    // Execute calculations in dependency order
    for (const calc of this.template.calculations) {
      const formula = this.replaceConstants(calc.formula, calc.constants);
      results[calc.id] = this.parser.evaluate(formula, context);
      context[calc.id] = results[calc.id]; // Make available for subsequent calcs
    }
    
    return results;
  }
  
  replaceConstants(formula, constants) {
    let result = formula;
    for (const [key, value] of Object.entries(constants)) {
      result = result.replace(new RegExp(key, 'g'), value.toString());
    }
    return result;
  }
}