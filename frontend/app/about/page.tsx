"use client"

import { useRouter } from 'next/navigation'
import { ArrowLeft, Info, CheckCircle2, Brain, Database, Globe } from 'lucide-react'
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { ScrollArea } from "@/components/ui/scroll-area"

export default function AboutPage() {
    const router = useRouter()

    const supportedBreeds = {
        Dog: [
            "Afghan", "African Wild Dog", "Golden Retriever", "Labrador", "German Shepherd",
            "Bulldog", "Poodle", "Beagle", "Husky", "Corgi"
        ],
        Cat: [
            "Abyssinian", "American Bobtail", "Persian", "Siamese", "Maine Coon",
            "Bengal", "Ragdoll", "British Shorthair", "Sphynx", "Scottish Fold"
        ],
        Fish: [
            "Goldfish", "Betta", "Clownfish", "Guppy", "Angelfish"
        ],
        Bird: [
            "Parrot", "Canary", "Cockatiel", "Parakeet", "Finch"
        ],
        Monkey: [
            "Capuchin", "Macaque", "Marmoset", "Spider Monkey", "Tamarin1"
        ]
    }

    return (
        <div className="min-h-screen bg-background">
            <div className="container mx-auto px-4 py-8 max-w-5xl">
                {/* Header */}
                <div className="flex items-center gap-4 mb-8">
                    <Button variant="ghost" size="icon" onClick={() => router.back()}>
                        <ArrowLeft className="h-6 w-6" />
                    </Button>
                    <div>
                        <h1 className="text-4xl font-bold tracking-tight">About the System</h1>
                        <p className="text-muted-foreground text-lg mt-1">
                            Understanding our AI-powered pet classification and pricing engine
                        </p>
                    </div>
                </div>

                <div className="grid gap-8 md:grid-cols-[2fr_1fr]">
                    <div className="space-y-8">
                        {/* How it Works */}
                        <section className="space-y-4">
                            <h2 className="text-2xl font-semibold flex items-center gap-2">
                                <Brain className="h-6 w-6 text-primary" />
                                How It Works
                            </h2>
                            <Card>
                                <CardContent className="pt-6 space-y-4">
                                    <div className="flex gap-4">
                                        <div className="h-10 w-10 rounded-full bg-primary/10 flex items-center justify-center shrink-0">
                                            <span className="font-bold text-primary">1</span>
                                        </div>
                                        <div>
                                            <h3 className="font-semibold mb-1">Image Analysis</h3>
                                            <p className="text-muted-foreground">
                                                Our advanced computer vision model (EfficientNetB0) analyzes your uploaded pet image to identify visual features specific to different breeds.
                                            </p>
                                        </div>
                                    </div>
                                    <div className="flex gap-4">
                                        <div className="h-10 w-10 rounded-full bg-primary/10 flex items-center justify-center shrink-0">
                                            <span className="font-bold text-primary">2</span>
                                        </div>
                                        <div>
                                            <h3 className="font-semibold mb-1">Breed Classification</h3>
                                            <p className="text-muted-foreground">
                                                The system classifies the pet into one of 5 types (Dog, Cat, Fish, Bird, Monkey) and identifies the specific breed with high accuracy.
                                            </p>
                                        </div>
                                    </div>
                                    <div className="flex gap-4">
                                        <div className="h-10 w-10 rounded-full bg-primary/10 flex items-center justify-center shrink-0">
                                            <span className="font-bold text-primary">3</span>
                                        </div>
                                        <div>
                                            <h3 className="font-semibold mb-1">Smart Pricing</h3>
                                            <p className="text-muted-foreground">
                                                Using metadata like age, weight, health status, and country of origin, our pricing model estimates a fair market value for the pet.
                                            </p>
                                        </div>
                                    </div>
                                </CardContent>
                            </Card>
                        </section>

                        {/* Supported Breeds */}
                        <section className="space-y-4">
                            <h2 className="text-2xl font-semibold flex items-center gap-2">
                                <Database className="h-6 w-6 text-primary" />
                                Supported Breeds
                            </h2>
                            <Card>
                                <CardHeader>
                                    <CardTitle>Breed Library</CardTitle>
                                    <CardDescription>
                                        Our system is currently trained to recognize the following breeds across 5 pet types.
                                    </CardDescription>
                                </CardHeader>
                                <CardContent>
                                    <Tabs defaultValue="Dog" className="w-full">
                                        <TabsList className="grid w-full grid-cols-5">
                                            {Object.keys(supportedBreeds).map((type) => (
                                                <TabsTrigger key={type} value={type}>{type}</TabsTrigger>
                                            ))}
                                        </TabsList>
                                        {Object.entries(supportedBreeds).map(([type, breeds]) => (
                                            <TabsContent key={type} value={type} className="mt-4">
                                                <ScrollArea className="h-[300px] w-full rounded-md border p-4">
                                                    <div className="grid grid-cols-2 gap-4">
                                                        {breeds.map((breed) => (
                                                            <div key={breed} className="flex items-center gap-2 p-2 rounded-lg hover:bg-muted transition-colors">
                                                                <CheckCircle2 className="h-4 w-4 text-green-500" />
                                                                <span>{breed}</span>
                                                            </div>
                                                        ))}
                                                    </div>
                                                </ScrollArea>
                                            </TabsContent>
                                        ))}
                                    </Tabs>
                                </CardContent>
                            </Card>
                        </section>
                    </div>

                    <div className="space-y-6">
                        {/* Stats Card */}
                        <Card className="bg-primary text-primary-foreground">
                            <CardHeader>
                                <CardTitle className="flex items-center gap-2">
                                    <Info className="h-5 w-5" />
                                    System Capabilities
                                </CardTitle>
                            </CardHeader>
                            <CardContent className="space-y-4">
                                <div className="flex justify-between items-center border-b border-primary-foreground/20 pb-2">
                                    <span>Pet Types</span>
                                    <span className="font-bold text-2xl">5</span>
                                </div>
                                <div className="flex justify-between items-center border-b border-primary-foreground/20 pb-2">
                                    <span>Total Breeds</span>
                                    <span className="font-bold text-2xl">
                                        {Object.values(supportedBreeds).reduce((acc, curr) => acc + curr.length, 0)}
                                    </span>
                                </div>
                                <div className="flex justify-between items-center">
                                    <span>Supported Countries</span>
                                    <span className="font-bold text-2xl">20+</span>
                                </div>
                            </CardContent>
                        </Card>

                        {/* Country Info */}
                        <Card>
                            <CardHeader>
                                <CardTitle className="flex items-center gap-2">
                                    <Globe className="h-5 w-5 text-primary" />
                                    Global Pricing
                                </CardTitle>
                            </CardHeader>
                            <CardContent>
                                <p className="text-sm text-muted-foreground mb-4">
                                    Our pricing model takes into account the country of origin. Certain breeds from specific regions may command higher prices due to rarity or lineage prestige.
                                </p>
                                <div className="text-sm font-medium">
                                    Example:
                                </div>
                                <ul className="list-disc list-inside text-sm text-muted-foreground mt-1 space-y-1">
                                    <li>Persian cats from Iran</li>
                                    <li>Siamese cats from Thailand</li>
                                    <li>German Shepherds from Germany</li>
                                </ul>
                            </CardContent>
                        </Card>
                    </div>
                </div>
            </div>
        </div>
    )
}
