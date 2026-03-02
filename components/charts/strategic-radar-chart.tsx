```tsx
"use client";

import React from "react";
import {
  Radar,
  RadarChart,
  PolarGrid,
  PolarAngleAxis,
  PolarRadiusAxis,
  ResponsiveContainer,
  Tooltip,
} from "recharts";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { cn } from "@/lib/utils"; // Assurez-vous que le fichier utilitaire est configuré

interface ChartData {
  category: string;
  scoreA: number;
  scoreB: number;
  fullMark: number;
}

interface StrategicRadarChartProps {
  data: ChartData[];
  className?: string;
}

/**
 * Composant client pour afficher un graphique radar stratégique.
 * Utilise Recharts pour la visualisation et Shadcn/ui pour la carte conteneur.
 */
export function StrategicRadarChart({ data, className }: StrategicRadarChartProps) {
  // Définition des couleurs pour le mode sombre
  const axisColor = "hsl(var(--muted-foreground))"; // Couleur pour les axes
  const gridColor = "hsl(var(--border))";         // Couleur pour la grille
  const categoryTextColor = "hsl(var(--foreground))"; // Couleur pour le texte des catégories

  return (
    <Card className={cn("w-full h-full bg-background border border-border text-foreground", className)}>
      <CardHeader>
        <CardTitle className="text-xl font-semibold text-center">Aperçu Stratégique</CardTitle>
      </CardHeader>
      <CardContent className="h-[calc(100%-80px)] p-4"> {/* Ajustez la hauteur si nécessaire */}
        <ResponsiveContainer width="100%" height="100%">
          <RadarChart outerRadius="70%" data={data}>
            <PolarGrid stroke={gridColor} />
            <PolarAngleAxis dataKey="category" stroke={categoryTextColor} tickLine={false} axisLine={false} />
            <PolarRadiusAxis angle={90} domain={[0, 150]} stroke={axisColor} tick={false} axisLine={false} />
            <Radar
              name="Score Actuel"
              dataKey="scoreA"
              stroke="hsl(var(--primary))"
              fill="hsl(var(--primary))"
              fillOpacity={0.6}
            />
            <Radar
              name="Objectif"
              dataKey="scoreB"
              stroke="hsl(var(--secondary))"
              fill="hsl(var(--secondary))"
              fillOpacity={0.4}
            />
            <Tooltip
              contentStyle={{
                backgroundColor: "hsl(var(--popover))",
                borderColor: "hsl(var(--border))",
                borderRadius: "var(--radius)",
                color: "hsl(var(--popover-foreground))",
              }}
              itemStyle={{
                color: "hsl(var(--popover-foreground))",
              }}
            />
          </RadarChart>
        </ResponsiveContainer>
      </CardContent>
    </Card>
  );
}
```