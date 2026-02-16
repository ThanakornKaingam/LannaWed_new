import React, { useEffect, useState } from "react";
import Image from "next/image";

const API_BASE =
  process.env.NEXT_PUBLIC_API_URL || "http://127.0.0.1:8000";

type PredictionResult = {
  class_name: string;
  confidence: number;
};

export default function Classify() {
  const [file, setFile] = useState<File | null>(null);
  const [preview, setPreview] = useState<string | null>(null);
  const [result, setResult] = useState<PredictionResult | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  /* ---------------- CLEAN PREVIEW ---------------- */

  useEffect(() => {
    return () => {
      if (preview) URL.revokeObjectURL(preview);
    };
  }, [preview]);

  /* ---------------- FILE CHANGE ---------------- */

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (!e.target.files) return;

    const selectedFile = e.target.files[0];

    if (preview) URL.revokeObjectURL(preview);

    setFile(selectedFile);
    setPreview(URL.createObjectURL(selectedFile));
    setResult(null);
    setError("");
  };

  /* ---------------- UPLOAD ---------------- */

  const handleUpload = async () => {
    if (!file) {
      setError("กรุณาเลือกรูปก่อน");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);

    try {
      setLoading(true);
      setError("");

      const res = await fetch(`${API_BASE}/predict/`, {
        method: "POST",
        body: formData,
      });

      if (!res.ok) {
        throw new Error("Prediction failed");
      }

      const data = await res.json();

      if (!data.class_name || data.confidence === undefined) {
        throw new Error("ผลลัพธ์จากโมเดลไม่ถูกต้อง");
      }

      setResult(data);
    } catch (err: any) {
      setError(err.message || "เกิดข้อผิดพลาดในการอัปโหลด");
    } finally {
      setLoading(false);
    }
  };

  /* ---------------- UI ---------------- */

  return (
    <div className="min-h-screen bg-gradient-to-br from-green-50 to-emerald-100 flex items-center justify-center p-6">
      <div className="bg-white shadow-2xl rounded-2xl p-8 w-full max-w-lg">
        <h1 className="text-3xl font-bold mb-6 text-center text-green-700">
          🌿 Vegetable Classification
        </h1>

        <input
          type="file"
          accept="image/*"
          onChange={handleFileChange}
          className="w-full border rounded-lg p-2 mb-4"
        />

        {preview && (
          <div className="mb-4 flex justify-center">
            <div className="relative w-64 h-64 rounded-lg overflow-hidden shadow">
              <Image
                src={preview}
                alt="preview"
                fill
                className="object-cover"
              />
            </div>
          </div>
        )}

        <button
          onClick={handleUpload}
          disabled={loading}
          className="w-full bg-green-600 hover:bg-green-700 text-white py-3 rounded-lg transition font-semibold disabled:opacity-60"
        >
          {loading ? "🔄 Predicting..." : "🚀 Predict"}
        </button>

        {error && (
          <div className="mt-4 text-red-500 text-center font-medium">
            {error}
          </div>
        )}

        {result && (
          <div className="mt-6 bg-gray-50 p-5 rounded-xl border shadow">
            <h3 className="text-lg font-bold mb-3 text-green-700 text-center">
              🎯 Prediction Result
            </h3>

            <div className="text-center mb-2">
              <p className="text-xl font-semibold">
                {result.class_name.replace(/_/g, " ")}
              </p>

              <p className="text-sm text-gray-500">
                Confidence: {(result.confidence * 100).toFixed(2)}%
              </p>
            </div>

            <div className="w-full bg-gray-200 rounded-full h-3 overflow-hidden">
              <div
                className="bg-green-500 h-3 transition-all"
                style={{ width: `${result.confidence * 100}%` }}
              />
            </div>
          </div>
        )}
      </div>
    </div>
  );
}