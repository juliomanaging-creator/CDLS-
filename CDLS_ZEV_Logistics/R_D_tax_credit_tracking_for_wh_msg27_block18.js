// Define schema:
const routeSchema = Joi.object({
  route_name: Joi.string().min(3).max(100).required(),
  origin_dealer_id: Joi.number().integer().positive().required(),
  destination_dealer_id: Joi.number().integer().positive().required(),
  total_distance_miles: Joi.number().positive().max(1000),
  waypoints: Joi.array().items(
    Joi.object({
      dealer_id: Joi.number().required(),
      sequence: Joi.number().required()
    })
  )
});

// Validate input:
const { error } = routeSchema.validate(userInput);
if (error) {
  // Reject: "route_name must be at least 3 characters"
}