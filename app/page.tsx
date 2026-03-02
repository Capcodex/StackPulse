```typescript
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card";
import { Sun, Moon } from "lucide-react"; // Exemple d'icônes Lucide-react
import { ModeToggle } from "@/components/mode-toggle"; // Composant pour basculer le thème

export default function Home() {
  return (
    <main className="flex min-h-screen flex-col items-center justify-center p-8 md:p-24 bg-background text-foreground">
      <div className="z-10 w-full max-w-5xl items-center justify-end font-mono text-sm flex mb-8 md:mb-16">
        <ModeToggle /> {/* Bouton pour changer de thème */}
      </div>

      <div className="flex flex-col items-center justify-center space-y-8">
        <h1 className="text-4xl sm:text-5xl font-bold tracking-tight lg:text-7xl text-center">
          Bienvenue sur votre App Next.js 15
        </h1>
        <p className="max-w-xl text-center text-lg text-muted-foreground">
          Cette application est initialisée avec Next.js 15, Tailwind CSS, Shadcn/ui et un thème Vercel-like Dark Mode.
        </p>

        <Button className="px-8 py-4 text-lg">
          Commencer l'exploration
        </Button>

        <Card className="w-full max-w-md mt-8">
          <CardHeader>
            <CardTitle>Votre Projet Minimaliste</CardTitle>
            <CardDescription>
              Une base solide et moderne pour vos futures fonctionnalités.
            </CardDescription>
          </CardHeader>
          <CardContent className="grid gap-4">
            <div className="flex items-center space-x-4 rounded-md border p-4">
              <Sun className="h-5 w-5" />
              <div className="flex-1 space-y-1">
                <p className="text-sm font-medium leading-none">
                  Thème Sombre par défaut
                </p>
                <p className="text-sm text-muted-foreground">
                  Conforme au design "Vercel-like".
                </p>
              </div>
            </div>
            <div className="flex items-center space-x-4 rounded-md border p-4">
              <Moon className="h-5 w-5" />
              <div className="flex-1 space-y-1">
                <p className="text-sm font-medium leading-none">
                  Shadcn/ui & Tailwind
                </p>
                <p className="text-sm text-muted-foreground">
                  Composants stylisés et personnalisables.
                </p>
              </div>
            </div>
          </CardContent>
          <CardFooter>
            <Button className="w-full">
              Voir la documentation
            </Button>
          </CardFooter>
        </Card>
      </div>
    </main>
  );
}
```