import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid,
  ResponsiveContainer,
} from "recharts";

function DemandForecastChart({ forecast }) {

  if (!forecast) {
    return null;
  }

  const shortTerm = forecast.short_term || [];
  const mediumTerm = forecast.medium_term || [];
  const longTerm = forecast.long_term || [];

  const chartData = [
    ...shortTerm.map((item) => ({
      date: item.Date,
      demand: Number(item.Forecast_Demand),
      horizon: "Short Term",
    })),

    ...mediumTerm.map((item) => ({
      date: item.Date,
      demand: Number(item.Forecast_Demand),
      horizon: "Medium Term",
    })),

    ...longTerm.map((item) => ({
      date: item.Date,
      demand: Number(item.Forecast_Demand),
      horizon: "Long Term",
    })),
  ];

  return (
    <div className="bg-white rounded-2xl shadow-md p-6 mb-8">

      <div className="mb-5">

        <h2 className="text-2xl font-bold">
           Demand Forecast Trend
        </h2>

        <p className="text-gray-500 mt-1">
          Forecasted demand across short, medium and long-term horizons.
        </p>

      </div>

      <ResponsiveContainer width="100%" height={400}>

        <LineChart
          data={chartData}
          margin={{
            top: 10,
            right: 20,
            left: 10,
            bottom: 10,
          }}
        >

          <CartesianGrid strokeDasharray="3 3" />

          <XAxis
            dataKey="date"
            tick={{ fontSize: 11 }}
          />

          <YAxis
            label={{
              value: "Demand (Units)",
              angle: -90,
              position: "insideLeft",
            }}
          />

          <Tooltip
            formatter={(value) => [
              `${Math.round(value)} units`,
              "Forecast Demand",
            ]}
            labelFormatter={(label) => `Date: ${label}`}
          />

          <Line
            type="monotone"
            dataKey="demand"
            stroke="#2563eb"
            strokeWidth={3}
            dot={{ r: 4 }}
            activeDot={{ r: 7 }}
          />

        </LineChart>

      </ResponsiveContainer>

    </div>
  );
}

export default DemandForecastChart;