```tsx
"use client";

import React from "react";
import { Radar } from "react-chartjs-2";
import {
  Chart as ChartJS,
  RadialLinearScale,
  PointElement,
  LineElement,
  Filler,
  Tooltip,
  Legend,
  ChartData,
  ChartOptions,
} from "chart.js";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { cn } from "@/lib/utils"; // Assurez-vous que le chemin est correct pour votre setup shadcn

// Enregistrer les composants de Chart.js nécessaires
ChartJS.register(
  RadialLinearScale,
  PointElement,
  LineElement,
  Filler,
  Tooltip,
  Legend
);

// --- Interfaces pour les données du graphique ---
export interface RadarChartDataPoint {
  label: string; // Ex: "Maturité", "Innovation", "Scalabilité"
  value: number; // Score pour cette étiquette
}

export interface StrategicRadarDataset {
  label: string; // Nom de la stratégie/entité (Ex: "Stratégie A")
  data: RadarChartDataPoint[];
  borderColor?: string;
  backgroundColor?: string;
}

export interface StrategicRadarChartProps {
  title?: string;
  description?: string;
  datasets: StrategicRadarDataset[];
  maxScore?: number; // Score maximal pour l'axe du radar (ex: 100)
  className?: string;
}

const defaultColors = [
  "rgba(139, 92, 246, 0.8)", // Violet clair
  "rgba(100, 100, 255, 0.8)", // Bleu
  "rgba(255, 100, 100, 0.8)", // Rouge
  "rgba(100, 255, 100, 0.8)", // Vert
  "rgba(255, 200, 100, 0.8)", // Orange
];

export function StrategicRadarChart({
  title,
  description,
  datasets,
  maxScore = 100,
  className,
}: StrategicRadarChartProps) {
  // Extraire toutes les étiquettes uniques de tous les datasets
  const allLabels = Array.from(
    new Set(datasets.flatMap((ds) => ds.data.map((dp) => dp.label)))
  );

  // Préparer les données pour Chart.js
  const chartJsData: ChartData<"radar"> = {
    labels: allLabels,
    datasets: datasets.map((ds, index) => {
      const colorIndex = index % defaultColors.length;
      const defaultBorderColor = defaultColors[colorIndex];
      const defaultBackgroundColor = defaultColors[colorIndex].replace("0.8", "0.2"); // Plus transparent

      return {
        label: ds.label,
        data: allLabels.map(
          (label) => ds.data.find((dp) => dp.label === label)?.value || 0
        ),
        backgroundColor: ds.backgroundColor || defaultBackgroundColor,
        borderColor: ds.borderColor || defaultBorderColor,
        borderWidth: 2,
        pointBackgroundColor: ds.borderColor || defaultBorderColor,
        pointBorderColor: "#fff",
        pointHoverBackgroundColor: "#fff",
        pointHoverBorderColor: ds.borderColor || defaultBorderColor,
      };
    }),
  };

  // Options de Chart.js pour un look Vercel-like (Dark mode, puriste)
  const chartJsOptions: ChartOptions<"radar"> = {
    responsive: true,
    maintainAspectRatio: true,
    plugins: {
      legend: {
        display: true,
        position: "bottom",
        labels: {
          color: "hsl(215, 27.9%, 60.1%)", // text-muted-foreground
          font: {
            size: 14,
            family: "Inter, sans-serif",
          },
        },
      },
      tooltip: {
        backgroundColor: "hsl(217.2 32.6% 17.5%)", // card background
        titleColor: "hsl(210, 40%, 98%)", // foreground
        bodyColor: "hsl(215, 27.9%, 60.1%)", // text-muted-foreground
        borderColor: "hsl(217.2 32.6% 17.5%)",
        borderWidth: 1,
        cornerRadius: 4,
        boxPadding: 4,
        titleFont: {
          size: 14,
          weight: "bold",
        },
        bodyFont: {
          size: 12,
        },
      },
    },
    scales: {
      r: {
        angleLines: {
          color: "hsl(217.2 32.6% 17.5%)", // Border de carte ou foreground plus clair
        },
        grid: {
          color: "hsl(217.2 32.6% 17.5%)", // Border de carte
        },
        pointLabels: {
          color: "hsl(215, 27.9%, 60.1%)", // text-muted-foreground
          font: {
            size: 13,
            family: "Inter, sans-serif",
          },
        },
        ticks: {
          backdropColor: "hsl(222.2 84% 4.9%)", // background principal du dark mode
          color: "hsl(215, 27.9%, 60.1%)", // text-muted-foreground
          font: {
            size: 10,
          },
          z: 1, // Assure que le texte est au-dessus des lignes
          display: true, // Affiche les ticks
          beginAtZero: true,
          stepSize: maxScore / 5, // Affiche 5 graduations principales
        },
        min: 0,
        max: maxScore,
      },
    },
  };

  return (
    <Card className={cn("w-full h-full", className)}>
      {title && (
        <CardHeader>
          <CardTitle className="text-xl font-semibold text-foreground">
            {title}
          </CardTitle>
          {description && (
            <p className="text-sm text-muted-foreground mt-1">
              {description}
            </p>
          )}
        </CardHeader>
      )}
      <CardContent className="flex items-center justify-center p-4 h-[calc(100%-80px)]"> {/* Ajuste la hauteur si titre/description sont présents */}
        <div className="relative w-full h-full flex items-center justify-center">
          <Radar data={chartJsData} options={chartJsOptions} />
        </div>
      </CardContent>
    </Card>
  );
}
```