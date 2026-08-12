const schema = Joi.object({
  email: Joi.string().email().required(),
  age: Joi.number().min(18).max(120),
  password: Joi.string().min(8).required()
});

schema.validate(userData); // Pass or fail