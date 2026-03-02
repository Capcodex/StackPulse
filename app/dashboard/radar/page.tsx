```tsx
import { Metadata } from "next";
import { StrategicRadarChart } from "@/components/charts/strategic-radar-chart"; // Assurez-vous du chemin correct
import { Separator } from "@/components/ui/separator";

export const metadata: Metadata = {
  title: "Radar Stratégique",
  description: "Visualisation des métriques stratégiques clés de l'entreprise.",
};

// Données de démonstration pour le graphique radar
// Dans une application réelle, ces données proviendraient d'une API ou d'une base de données.
const chartData = [
  { category: "Innovation Technologique", scoreA: 95, scoreB: 120, fullMark: 150 },
  { category: "Pénétration du Marché", scoreA: 80, scoreB: 100, fullMark: 150 },
  { category: "Satisfaction Client", scoreA: 110, scoreB: 130, fullMark: 150 },
  { category: "Efficacité Opérationnelle", scoreA: 70, scoreB: 90, fullMark: 150 },
  { category: "Gestion des Risques", scoreA: 100, scoreB: 115, fullMark: 150 },
  { category: "Croissance des Revenus", scoreA: 85, scoreB: 110, fullMark: 150 },
];

/**
 * Page serveur dédiée à l'affichage du radar stratégique.
 * Cette page intègre le composant client StrategicRadarChart.
 */
export default function StrategicRadarPage() {
  return (
    <div className="flex-1 space-y-8 p-8 pt-6">
      <div className="flex items-center justify-between space-y-2">
        <h2 className="text-3xl font-bold tracking-tight text-foreground">Radar Stratégique</h2>
      </div>
      <p className="text-muted-foreground text-sm">
        Explorez les performances de l'entreprise à travers différentes dimensions stratégiques.
      </p>
      <Separator className="bg-border" />
      <div className="grid h-[600px] gap-4"> {/* Ajustez la hauteur selon les besoins */}
        <StrategicRadarChart data={chartData} />
      </div>
    </div>
  );
}
```