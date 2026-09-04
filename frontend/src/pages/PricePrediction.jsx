import { useState } from "react";
import { predictPrice } from "../services/predictionService";

function PricePrediction() {
  const [formData, setFormData] = useState({
    category: 0,
    original_price: "",
    discount: "",
    payment_method: 0,
    year: 2024,
    month: 1,
    day: 1,
  });

  const [result, setResult] = useState(null);

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: Number(e.target.value),
    });
  };

  const handlePredict = async () => {
    try {
      const data = await predictPrice(formData);
      setResult(data);
    } catch (error) {
      console.error(error);
      alert("Prediction Failed");
    }
  };

  return (
    <div className="max-w-4xl mx-auto p-8">

      <h1 className="text-4xl font-bold text-center mb-8">
         Dynamic Price Optimization Dashboard
      </h1>

      {/* ================= FORM ================= */}

      <div className="bg-white rounded-xl shadow-md p-6">

        <h2 className="text-2xl font-bold mb-5">
          Product Details
        </h2>

        <div className="space-y-4">

          <div>
            <label>Category</label>

            <select
              name="category"
              onChange={handleChange}
              className="border p-2 rounded w-full"
            >
              <option value={0}>Electronics</option>
              <option value={1}>Fashion</option>
              <option value={2}>Furniture</option>
              <option value={3}>Grocery</option>
            </select>
          </div>

          <div>
            <label>Original Price</label>

            <input
              type="number"
              name="original_price"
              onChange={handleChange}
              className="border p-2 rounded w-full"
            />
          </div>

          <div>
            <label>Discount (%)</label>

            <input
              type="number"
              name="discount"
              onChange={handleChange}
              className="border p-2 rounded w-full"
            />
          </div>

          <div>
            <label>Payment Method</label>

            <select
              name="payment_method"
              onChange={handleChange}
              className="border p-2 rounded w-full"
            >
              <option value={0}>Card</option>
              <option value={1}>Cash</option>
              <option value={2}>UPI</option>
            </select>
          </div>

          <div className="grid grid-cols-3 gap-4">

            <input
              type="number"
              name="year"
              value={formData.year}
              onChange={handleChange}
              className="border p-2 rounded"
            />

            <input
              type="number"
              name="month"
              value={formData.month}
              onChange={handleChange}
              className="border p-2 rounded"
            />

            <input
              type="number"
              name="day"
              value={formData.day}
              onChange={handleChange}
              className="border p-2 rounded"
            />

          </div>

          <button
            onClick={handlePredict}
            className="w-full bg-blue-600 text-white py-3 rounded-lg hover:bg-blue-700"
          >
            Predict Price
          </button>

        </div>

      </div>

      {/* ================= RESULTS ================= */}

      {result && (

        <>

          {/* AI Pricing Intelligence */}

          <div className="mt-8 bg-white rounded-xl shadow-md p-6">

            <h2 className="text-2xl font-bold mb-6">
               AI Pricing Intelligence
            </h2>

            <div className="grid grid-cols-2 gap-5">

              <div>
                <p className="text-gray-500">Predicted Price</p>
                <h3 className="text-2xl font-bold text-green-600">
                  ₹ {result.predicted_price}
                </h3>
              </div>

              <div>
                <p className="text-gray-500">Recommended Price</p>
                <h3 className="text-2xl font-bold text-blue-600">
                  ₹ {result.recommended_price}
                </h3>
              </div>

              <div>
                <p className="text-gray-500">Expected Demand</p>
                <h3 className="text-xl font-bold">
                  {result.expected_demand} Units
                </h3>
              </div>

              <div>
                <p className="text-gray-500">Expected Revenue</p>
                <h3 className="text-xl font-bold">
                  ₹ {result.expected_revenue}
                </h3>
              </div>

              <div>
                <p className="text-gray-500">Trend</p>
                <h3 className="text-xl font-bold">
                  {result.trend}
                </h3>
              </div>

              <div>
                <p className="text-gray-500">Confidence</p>
                <h3 className="text-xl font-bold">
                  {result.confidence}%
                </h3>
              </div>

            </div>

          </div>

          {/* Recommendation */}

          <div className="mt-8 bg-blue-100 rounded-xl shadow-md p-6">

            <h2 className="text-2xl font-bold mb-3">
               AI Recommendation
            </h2>

            <p>{result.recommendation}</p>

          </div>

          {/* Revenue Summary */}

          <div className="mt-8 bg-white rounded-xl shadow-md p-6">

            <h2 className="text-2xl font-bold mb-5">
               Revenue Optimization Summary
            </h2>

            <div className="grid grid-cols-2 gap-5">

              <div className="bg-green-50 rounded-lg p-4">
                <p>Candidate Prices Evaluated</p>
                <h2 className="text-2xl font-bold">
                  {result.optimization_results.length}
                </h2>
              </div>

              <div className="bg-blue-50 rounded-lg p-4">
                <p>Best Price</p>
                <h2 className="text-2xl font-bold">
                  ₹ {result.recommended_price}
                </h2>
              </div>

              <div className="bg-yellow-50 rounded-lg p-4">
                <p>Expected Demand</p>
                <h2 className="text-2xl font-bold">
                  {result.expected_demand}
                </h2>
              </div>

              <div className="bg-purple-50 rounded-lg p-4">
                <p>Maximum Revenue</p>
                <h2 className="text-2xl font-bold">
                  ₹ {result.expected_revenue}
                </h2>
              </div>

            </div>

          </div>

          {/* Decision Factors */}

          <div className="mt-8 bg-white rounded-xl shadow-md p-6">

            <h2 className="text-2xl font-bold mb-5">
               AI Decision Factors
            </h2>

            {Object.entries(result.feature_importance).map(([feature, value]) => (

              <div key={feature} className="mb-5">

                <div className="flex justify-between mb-2">

                  <span>{feature}</span>

                  <span className="font-semibold">
                    {value}%
                  </span>

                </div>

                <div className="w-full bg-gray-200 rounded-full h-3">

                  <div
                    className="bg-blue-600 h-3 rounded-full"
                    style={{ width: `${value}%` }}
                  ></div>

                </div>

              </div>

            ))}

          </div>

          {/* AI Insights */}

          <div className="mt-8 bg-white rounded-xl shadow-md p-6">

            <h2 className="text-2xl font-bold mb-5">
              💡 AI Insights
            </h2>

            <ul className="list-disc pl-5 space-y-3">

              <li>
                Original Price contributed{" "}
                <strong>
                  {result.feature_importance["Original Price"]}%
                </strong>{" "}
                to the prediction.
              </li>

              <li>
                Discount contributed{" "}
                <strong>
                  {result.feature_importance["Discount"]}%
                </strong>.
              </li>

              <li>
                AI evaluated{" "}
                <strong>
                  {result.optimization_results.length}
                </strong>{" "}
                candidate prices.
              </li>

              <li>
                Recommended selling price is{" "}
                <strong>
                  ₹ {result.recommended_price}
                </strong>.
              </li>

              <li>
                Current demand trend is{" "}
                <strong>
                  {result.trend}
                </strong>.
              </li>

            </ul>

          </div>

          {/* Workflow */}

          <div className="mt-8 bg-white rounded-xl shadow-md p-6">

            <h2 className="text-2xl font-bold mb-5">
             How AI Made This Decision
            </h2>

            <div className="space-y-4 text-center">

              <div className="bg-blue-50 p-4 rounded-lg">
               Product Details
              </div>

              <div>⬇️</div>

              <div className="bg-green-50 p-4 rounded-lg">
               Price Prediction Model
              </div>

              <div>⬇️</div>

              <div className="bg-yellow-50 p-4 rounded-lg">
               Demand Prediction Model
              </div>

              <div>⬇️</div>

              <div className="bg-purple-50 p-4 rounded-lg">
               Revenue Optimization Engine
              </div>

              <div>⬇️</div>

              <div className="bg-red-50 p-4 rounded-lg font-bold">
                AI Recommended Price
              </div>

            </div>

          </div>

        </>

      )}


{/* ================= MODEL PERFORMANCE ================= */}

<div className="mt-8 bg-white rounded-xl shadow-md p-6">

  <h2 className="text-2xl font-bold mb-5">
    📊 Model Performance
  </h2>

  <p className="text-gray-600 mb-5">
    Price prediction model evaluation on the validation dataset.
  </p>

  <div className="grid grid-cols-3 gap-5">

    <div className="bg-blue-50 rounded-lg p-5 text-center">
      <p className="text-gray-600">MAE</p>
      <h3 className="text-2xl font-bold">
        0.76
      </h3>
    </div>

    <div className="bg-green-50 rounded-lg p-5 text-center">
      <p className="text-gray-600">RMSE</p>
      <h3 className="text-2xl font-bold">
        1.07
      </h3>
    </div>

    <div className="bg-purple-50 rounded-lg p-5 text-center">
      <p className="text-gray-600">R² Score</p>
      <h3 className="text-2xl font-bold">
        0.9999
      </h3>
    </div>

  </div>

  <div className="mt-5 bg-yellow-50 border border-yellow-200 rounded-lg p-4">

    <p className="text-sm text-gray-700">
      <strong>Evaluation:</strong> The model was evaluated using an
      80/20 train-test split. These metrics describe prediction
      performance on the validation data.
    </p>

  </div>

</div>
    </div>
  );
}

export default PricePrediction;