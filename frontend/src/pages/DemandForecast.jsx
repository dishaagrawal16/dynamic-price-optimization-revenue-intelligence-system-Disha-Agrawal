
import { useEffect, useState } from "react";
import { getDemandForecast } from "../services/forecastService";
import DemandForecastChart from "../components/DemandForecastChart";

function DemandForecast() {

  const [forecast, setForecast] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {

    const loadForecast = async () => {

      try {

        const data = await getDemandForecast();

        setForecast(data);

      } catch (err) {

        console.error(err);

        setError(
          "Unable to load demand forecast."
        );

      } finally {

        setLoading(false);

      }
    };

    loadForecast();

  }, []);

  if (loading) {

    return (
      <div className="p-8 text-center">
        Loading demand forecast...
      </div>
    );

  }

  if (error) {

    return (
      <div className="p-8 text-center text-red-600">
        {error}
      </div>
    );

  }

  return (

    <div className="max-w-6xl mx-auto p-8">

      {/* PAGE HEADER */}

      <div className="mb-8">

        <h1 className="text-3xl font-bold">
          AI Demand Forecast
        </h1>

        <p className="text-gray-500 mt-2">
          Predictive demand intelligence based on
          historical sales patterns and seasonality.
        </p>

      </div>


      {/* SUMMARY CARDS */}

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">

      <DemandForecastChart forecast={forecast} />

        {/* TREND */}

        <div className="bg-white rounded-xl shadow-md p-6">

          <p className="text-gray-500">
            Current Demand Trend
          </p>

          <h2 className="text-3xl font-bold mt-2">

            {forecast.trend}

          </h2>

        </div>


        {/* RELIABILITY */}

        <div className="bg-white rounded-xl shadow-md p-6">

          <p className="text-gray-500">
            Forecast Reliability
          </p>

          <h2 className="text-3xl font-bold mt-2 text-blue-600">

            {forecast.reliability_score}%

          </h2>

        </div>

      </div>

            {/* ================= MODEL VALIDATION ================= */}

      <div className="bg-white rounded-xl shadow-md p-6 mb-8">

        <h2 className="text-2xl font-bold mb-2">
          📊 Forecast Model Performance
        </h2>

        <p className="text-gray-500 mb-5">
          Evaluation results from chronological validation of the
          demand forecasting model.
        </p>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-5">

          {/* MAE */}

          <div className="bg-blue-50 rounded-lg p-5 text-center">

            <p className="text-gray-600">
              MAE
            </p>

            <h3 className="text-2xl font-bold mt-1">
              528.46
            </h3>

            <p className="text-xs text-gray-500 mt-1">
              units
            </p>

          </div>


          {/* RMSE */}

          <div className="bg-green-50 rounded-lg p-5 text-center">

            <p className="text-gray-600">
              RMSE
            </p>

            <h3 className="text-2xl font-bold mt-1">
              683.82
            </h3>

            <p className="text-xs text-gray-500 mt-1">
              units
            </p>

          </div>


          {/* R2 */}

          <div className="bg-purple-50 rounded-lg p-5 text-center">

            <p className="text-gray-600">
              R² Score
            </p>

            <h3 className="text-2xl font-bold mt-1">
              -0.3746
            </h3>

          </div>

        </div>


        {/* BASELINE COMPARISON */}

        <div className="mt-6">

          <h3 className="text-lg font-semibold mb-3">
            Baseline Comparison
          </h3>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">

            <div className="bg-gray-50 rounded-lg p-4">

              <p className="text-gray-600">
                MAE Improvement
              </p>

              <p className="text-2xl font-bold text-green-600">
                17.8%
              </p>

              <p className="text-sm text-gray-500">
                vs. naive baseline
              </p>

            </div>


            <div className="bg-gray-50 rounded-lg p-4">

              <p className="text-gray-600">
                RMSE Improvement
              </p>

              <p className="text-2xl font-bold text-green-600">
                12.4%
              </p>

              <p className="text-sm text-gray-500">
                vs. naive baseline
              </p>

            </div>

          </div>

        </div>


        {/* EVALUATION NOTE */}

        <div className="mt-5 bg-yellow-50 border border-yellow-200 rounded-lg p-4">

          <p className="text-sm text-gray-700">

            <strong>Evaluation:</strong> Random Forest improved
            MAE and RMSE compared with the naive baseline.
            However, the negative R² score indicates that the
            current dataset provides limited predictive signal
            and additional data would be needed for
            production-grade forecasting.

          </p>

        </div>

      </div>


      {/* SHORT TERM */}

      <div className="bg-white rounded-xl shadow-md p-6 mb-8">

        <div className="mb-5">

          <h2 className="text-2xl font-bold">
             Short-Term Forecast
          </h2>

          <p className="text-gray-500">
            Expected demand for the next 7 days
          </p>

        </div>


        <div className="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-7 gap-4">

          {forecast.short_term.map(
            (item, index) => (

              <div
                key={index}
                className="bg-blue-50 rounded-lg p-4 text-center"
              >

                <p className="text-sm text-gray-500">
                  {item.Date}
                </p>

                <p className="text-xl font-bold mt-2">
                  {Math.round(
                    item.Forecast_Demand
                  )}
                </p>

                <p className="text-xs text-gray-500">
                  units
                </p>

              </div>

            )
          )}

        </div>

      </div>


      {/* MEDIUM + LONG TERM */}

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">

        {/* MEDIUM TERM */}

        <div className="bg-white rounded-xl shadow-md p-6">

          <h2 className="text-2xl font-bold mb-2">
             Medium-Term Forecast
          </h2>

          <p className="text-gray-500 mb-5">
            Expected demand over the next 4 weeks
          </p>

          <div className="space-y-3">

            {forecast.medium_term.map(
              (item, index) => (

                <div
                  key={index}
                  className="flex justify-between items-center
                             bg-gray-50 p-4 rounded-lg"
                >

                  <span>
                    {item.Date}
                  </span>

                  <span className="font-bold">
                    {Math.round(
                      item.Forecast_Demand
                    )} units
                  </span>

                </div>

              )
            )}

          </div>

        </div>


        {/* LONG TERM */}

        <div className="bg-white rounded-xl shadow-md p-6">

          <h2 className="text-2xl font-bold mb-2">
             Long-Term Forecast
          </h2>

          <p className="text-gray-500 mb-5">
            Expected demand over the next 3 months
          </p>

          <div className="space-y-3">

            {forecast.long_term.map(
              (item, index) => (

                <div
                  key={index}
                  className="flex justify-between items-center
                             bg-gray-50 p-4 rounded-lg"
                >

                  <span>
                    {item.Date}
                  </span>

                  <span className="font-bold">
                    {Math.round(
                      item.Forecast_Demand
                    )} units
                  </span>

                </div>

              )
            )}

          </div>

        </div>

      </div>

    </div>

  );

}

export default DemandForecast;