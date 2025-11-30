"use client"

import { useState, useEffect, useRef } from "react"
import { useRouter } from "next/navigation"
import { Upload, Brain, CheckCircle2, AlertCircle, Loader2, Info, RefreshCw, PlusCircle } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Alert, AlertDescription, AlertTitle } from "@/components/ui/alert"
import { useToast } from "@/components/ui/use-toast"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import {
    Dialog,
    DialogContent,
    DialogDescription,
    DialogHeader,
    DialogTitle,
    DialogTrigger,
} from "@/components/ui/dialog"

const PRODUCT_TYPES = ["Dog", "Cat", "Fish", "Bird", "Monkey"]

export default function TrainModelPage() {
    const router = useRouter()
    const { toast } = useToast()

    const [isLoading, setIsLoading] = useState(false)
    const [isTraining, setIsTraining] = useState(false)

    // Form State
    const [mode, setMode] = useState<"add" | "fine_tune">("add")
    const [productType, setProductType] = useState("")
    const [breedName, setBreedName] = useState("") // For Add Mode
    const [selectedBreed, setSelectedBreed] = useState("") // For Fine-Tune Mode
    const [file, setFile] = useState<File | null>(null)

    // Data State
    const [existingBreeds, setExistingBreeds] = useState<string[]>([])
    const [loadingBreeds, setLoadingBreeds] = useState(false)

    // Console State
    const [status, setStatus] = useState<{ type: 'success' | 'error' | 'info', message: string } | null>(null)
    const [logs, setLogs] = useState<string[]>([])
    const logsEndRef = useRef<HTMLDivElement>(null)

    // Fetch breeds when type changes in Fine-Tune mode
    useEffect(() => {
        if (mode === "fine_tune" && productType) {
            const fetchBreeds = async () => {
                setLoadingBreeds(true)
                try {
                    const res = await fetch(`http://localhost:8000/train/breeds/${productType}`)
                    const data = await res.json()
                    setExistingBreeds(data.breeds || [])
                } catch (err) {
                    console.error("Failed to fetch breeds", err)
                    toast({
                        title: "Error fetching breeds",
                        description: "Could not load existing breeds for this type.",
                        variant: "destructive"
                    })
                } finally {
                    setLoadingBreeds(false)
                }
            }
            fetchBreeds()
        }
    }, [mode, productType, toast])

    // Polling for logs
    useEffect(() => {
        let interval: NodeJS.Timeout

        if (isTraining) {
            interval = setInterval(async () => {
                try {
                    const response = await fetch("http://localhost:8000/train/status")
                    const data = await response.json()

                    if (data.logs) {
                        setLogs(data.logs)
                    }

                    if (data.status === "completed") {
                        setIsTraining(false)
                        toast({
                            title: "Training Complete",
                            description: "The model has been successfully updated.",
                        })
                        setStatus({
                            type: 'success',
                            message: "Training completed successfully!"
                        })
                    } else if (data.status === "error") {
                        setIsTraining(false)
                        setStatus({
                            type: 'error',
                            message: "Training failed. Check logs for details."
                        })
                    }
                } catch (error) {
                    console.error("Error fetching status:", error)
                }
            }, 2000)
        }

        return () => clearInterval(interval)
    }, [isTraining, toast])

    // Auto-scroll logs
    useEffect(() => {
        logsEndRef.current?.scrollIntoView({ behavior: "smooth" })
    }, [logs])

    const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        if (e.target.files && e.target.files[0]) {
            const selectedFile = e.target.files[0]
            if (!selectedFile.name.endsWith('.zip')) {
                toast({
                    title: "Invalid file type",
                    description: "Please upload a ZIP file containing images.",
                    variant: "destructive"
                })
                return
            }
            setFile(selectedFile)
        }
    }

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault()

        // Validation
        if (!productType || !file) {
            toast({ title: "Missing fields", description: "Please fill in all fields.", variant: "destructive" })
            return
        }

        const finalBreedName = mode === "add" ? breedName : selectedBreed
        if (!finalBreedName) {
            toast({ title: "Missing Breed Name", description: "Please specify the breed.", variant: "destructive" })
            return
        }

        setIsLoading(true)
        setStatus(null)
        setLogs([])

        try {
            const formData = new FormData()
            formData.append("breed_name", finalBreedName)
            formData.append("product_type", productType)
            formData.append("images_zip", file)

            const response = await fetch("http://localhost:8000/train/add-breed", {
                method: "POST",
                body: formData,
            })

            const data = await response.json()

            if (!response.ok) {
                throw new Error(data.detail || "Failed to start training")
            }

            setStatus({
                type: 'success',
                message: data.message
            })

            toast({
                title: "Training Started",
                description: "The model is being updated in the background.",
            })

            setIsTraining(true)

            // Reset form partially
            setFile(null)
            if (mode === "add") setBreedName("")

        } catch (error) {
            console.error("Training error:", error)
            setStatus({
                type: 'error',
                message: error instanceof Error ? error.message : "An unexpected error occurred"
            })
        } finally {
            setIsLoading(false)
        }
    }

    return (
        <div className="container mx-auto px-4 py-8 max-w-3xl">
            <div className="flex items-center justify-between mb-8">
                <div className="flex items-center gap-4">
                    <div className="h-12 w-12 rounded-lg bg-primary/10 flex items-center justify-center">
                        <Brain className="h-6 w-6 text-primary" />
                    </div>
                    <div>
                        <h1 className="text-3xl font-bold tracking-tight">Train Model</h1>
                        <p className="text-muted-foreground">
                            Manage your AI model's knowledge base
                        </p>
                    </div>
                </div>

                <Dialog>
                    <DialogTrigger asChild>
                        <Button variant="outline" size="sm">
                            <Info className="mr-2 h-4 w-4" />
                            How it works
                        </Button>
                    </DialogTrigger>
                    <DialogContent className="max-w-2xl">
                        <DialogHeader>
                            <DialogTitle>Training Modes Explained</DialogTitle>
                            <DialogDescription>
                                Understanding the difference between adding breeds and fine-tuning.
                            </DialogDescription>
                        </DialogHeader>
                        <div className="grid gap-4 py-4">
                            <div className="grid grid-cols-[25px_1fr] items-start pb-4 border-b last:border-0">
                                <span className="flex h-2 w-2 translate-y-1 rounded-full bg-blue-500" />
                                <div className="space-y-1">
                                    <p className="text-sm font-medium leading-none">Add New Breed (Model Surgery)</p>
                                    <p className="text-sm text-muted-foreground">
                                        Use this when you want to teach the AI a **completely new** breed it has never seen before (e.g., adding "Pug" to a model that only knows "Bulldog").
                                        <br /><br />
                                        <strong>Technique:</strong> The system expands the neural network's output layer, copies existing knowledge, and initializes new connections for the new breed.
                                    </p>
                                </div>
                            </div>
                            <div className="grid grid-cols-[25px_1fr] items-start pb-4 last:border-0">
                                <span className="flex h-2 w-2 translate-y-1 rounded-full bg-green-500" />
                                <div className="space-y-1">
                                    <p className="text-sm font-medium leading-none">Fine-Tune Existing (Accuracy Boost)</p>
                                    <p className="text-sm text-muted-foreground">
                                        Use this when the AI already knows a breed but makes mistakes (e.g., confusing Akita Inu with Shiba Inu).
                                        <br /><br />
                                        <strong>Technique:</strong> The system retrains the existing model with your new images to refine its accuracy without changing the model structure.
                                    </p>
                                </div>
                            </div>
                        </div>
                    </DialogContent>
                </Dialog>
            </div>

            <Card>
                <CardHeader>
                    <CardTitle>Training Configuration</CardTitle>
                    <CardDescription>
                        Choose your training strategy and upload data.
                    </CardDescription>
                </CardHeader>
                <CardContent>
                    <Tabs value={mode} onValueChange={(v) => setMode(v as "add" | "fine_tune")} className="w-full">
                        <TabsList className="grid w-full grid-cols-2 mb-6">
                            <TabsTrigger value="add" className="flex items-center gap-2">
                                <PlusCircle className="h-4 w-4" />
                                Add New Breed
                            </TabsTrigger>
                            <TabsTrigger value="fine_tune" className="flex items-center gap-2">
                                <RefreshCw className="h-4 w-4" />
                                Fine-Tune Existing
                            </TabsTrigger>
                        </TabsList>

                        <form onSubmit={handleSubmit} className="space-y-6">
                            <div className="space-y-2">
                                <Label htmlFor="type">Product Type</Label>
                                <Select value={productType} onValueChange={setProductType}>
                                    <SelectTrigger>
                                        <SelectValue placeholder="Select a type (e.g. Dog)" />
                                    </SelectTrigger>
                                    <SelectContent>
                                        {PRODUCT_TYPES.map((type) => (
                                            <SelectItem key={type} value={type}>
                                                {type}
                                            </SelectItem>
                                        ))}
                                    </SelectContent>
                                </Select>
                            </div>

                            <TabsContent value="add" className="space-y-4 mt-0">
                                <div className="space-y-2">
                                    <Label htmlFor="breed">New Breed Name</Label>
                                    <Input
                                        id="breed"
                                        placeholder="e.g. Golden Retriever"
                                        value={breedName}
                                        onChange={(e) => setBreedName(e.target.value)}
                                    />
                                    <p className="text-xs text-muted-foreground">
                                        This will create a new category in the AI model.
                                    </p>
                                </div>
                            </TabsContent>

                            <TabsContent value="fine_tune" className="space-y-4 mt-0">
                                <div className="space-y-2">
                                    <Label htmlFor="existing-breed">Select Breed to Improve</Label>
                                    <Select value={selectedBreed} onValueChange={setSelectedBreed} disabled={!productType || loadingBreeds}>
                                        <SelectTrigger>
                                            <SelectValue placeholder={!productType ? "Select Type first" : loadingBreeds ? "Loading..." : "Select a breed"} />
                                        </SelectTrigger>
                                        <SelectContent>
                                            {existingBreeds.map((breed) => (
                                                <SelectItem key={breed} value={breed}>
                                                    {breed}
                                                </SelectItem>
                                            ))}
                                        </SelectContent>
                                    </Select>
                                    {!productType && (
                                        <p className="text-xs text-yellow-600">
                                            Please select a Product Type above to see available breeds.
                                        </p>
                                    )}
                                </div>
                            </TabsContent>

                            <div className="space-y-2">
                                <Label htmlFor="file">Training Images (ZIP)</Label>
                                <div className="border-2 border-dashed rounded-lg p-6 hover:bg-muted/50 transition-colors text-center cursor-pointer relative">
                                    <input
                                        type="file"
                                        id="file"
                                        accept=".zip"
                                        className="absolute inset-0 w-full h-full opacity-0 cursor-pointer"
                                        onChange={handleFileChange}
                                    />
                                    <div className="flex flex-col items-center gap-2">
                                        <Upload className="h-8 w-8 text-muted-foreground" />
                                        {file ? (
                                            <span className="font-medium text-primary">{file.name}</span>
                                        ) : (
                                            <span className="text-muted-foreground">Drop ZIP file here or click to upload</span>
                                        )}
                                    </div>
                                </div>
                            </div>

                            {status && (
                                <Alert variant={status.type === 'error' ? "destructive" : "default"} className={status.type === 'success' ? "border-green-500 text-green-600 bg-green-50" : ""}>
                                    {status.type === 'error' ? <AlertCircle className="h-4 w-4" /> : <CheckCircle2 className="h-4 w-4" />}
                                    <AlertTitle>{status.type === 'error' ? "Error" : "Success"}</AlertTitle>
                                    <AlertDescription>
                                        {status.message}
                                    </AlertDescription>
                                </Alert>
                            )}

                            <Button type="submit" className="w-full" disabled={isLoading || isTraining}>
                                {isLoading ? (
                                    <>
                                        <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                                        Starting...
                                    </>
                                ) : isTraining ? (
                                    <>
                                        <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                                        Training in Progress...
                                    </>
                                ) : (
                                    <>
                                        <Brain className="mr-2 h-4 w-4" />
                                        {mode === "add" ? "Start Training (Add Breed)" : "Start Fine-Tuning"}
                                    </>
                                )}
                            </Button>
                        </form>
                    </Tabs>
                </CardContent>
            </Card>

            {/* Console Output */}
            <Card className="mt-8 bg-black text-green-400 font-mono text-sm shadow-xl border-green-900/50">
                <CardHeader className="border-b border-green-900/30 pb-2 bg-green-950/10">
                    <CardTitle className="text-sm font-normal flex items-center gap-2">
                        <div className={`h-2 w-2 rounded-full ${isTraining ? 'bg-green-500 animate-pulse' : 'bg-gray-500'}`} />
                        Training Console
                    </CardTitle>
                </CardHeader>
                <CardContent className="p-4 h-[300px] overflow-y-auto space-y-1 bg-black/95">
                    {logs.length === 0 ? (
                        <div className="text-green-900 italic">Waiting for logs...</div>
                    ) : (
                        logs.map((log, i) => (
                            <div key={i} className="break-all hover:bg-green-900/10 px-1 rounded">
                                <span className="opacity-50 mr-2 select-none">$</span>
                                {log}
                            </div>
                        ))
                    )}
                    <div ref={logsEndRef} />
                </CardContent>
            </Card>
        </div>
    )
}
