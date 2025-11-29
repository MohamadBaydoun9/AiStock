"use client"

import { useState, useEffect } from "react"
import { Plus, Edit, Trash2, Loader2, Package } from 'lucide-react'
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import {
    Table,
    TableBody,
    TableCell,
    TableHead,
    TableHeader,
    TableRow,
} from "@/components/ui/table"
import {
    Dialog,
    DialogContent,
    DialogDescription,
    DialogFooter,
    DialogHeader,
    DialogTitle,
} from "@/components/ui/dialog"
import {
    AlertDialog,
    AlertDialogAction,
    AlertDialogCancel,
    AlertDialogContent,
    AlertDialogDescription,
    AlertDialogFooter,
    AlertDialogHeader,
    AlertDialogTitle,
} from "@/components/ui/alert-dialog"
import { useToast } from "@/hooks/use-toast"
import { api, ProductType } from "@/lib/api"
import AuthGuard from "@/components/auth-guard"

export default function ProductTypesPage() {
    const { toast } = useToast()
    const [types, setTypes] = useState<ProductType[]>([])
    const [isLoading, setIsLoading] = useState(true)
    const [isDialogOpen, setIsDialogOpen] = useState(false)
    const [isDeleteDialogOpen, setIsDeleteDialogOpen] = useState(false)
    const [editingType, setEditingType] = useState<ProductType | null>(null)
    const [typeToDelete, setTypeToDelete] = useState<ProductType | null>(null)
    const [typeName, setTypeName] = useState("")
    const [isSaving, setIsSaving] = useState(false)

    useEffect(() => {
        fetchTypes()
    }, [])

    const fetchTypes = async () => {
        setIsLoading(true)
        try {
            const data = await api.getProductTypes()
            setTypes(data)
        } catch (error) {
            toast({
                title: "Error",
                description: "Failed to load product types",
                variant: "destructive"
            })
        } finally {
            setIsLoading(false)
        }
    }

    const handleOpenDialog = (type?: ProductType) => {
        if (type) {
            setEditingType(type)
            setTypeName(type.name)
        } else {
            setEditingType(null)
            setTypeName("")
        }
        setIsDialogOpen(true)
    }

    const handleCloseDialog = () => {
        setIsDialogOpen(false)
        setEditingType(null)
        setTypeName("")
    }

    const handleSave = async () => {
        if (!typeName.trim()) {
            toast({
                title: "Invalid Name",
                description: "Please enter a type name",
                variant: "destructive"
            })
            return
        }

        setIsSaving(true)
        try {
            if (editingType) {
                // Update existing type
                await api.updateProductType(editingType.type_id, typeName.trim())
                toast({
                    title: "Type Updated",
                    description: `"${typeName}" has been updated successfully`,
                })
            } else {
                // Create new type
                await api.createProductType(typeName.trim())
                toast({
                    title: "Type Created",
                    description: `"${typeName}" has been added successfully`,
                })
            }
            handleCloseDialog()
            fetchTypes()
        } catch (error: any) {
            toast({
                title: "Error",
                description: error.message || "Failed to save product type",
                variant: "destructive"
            })
        } finally {
            setIsSaving(false)
        }
    }

    const handleDeleteClick = (type: ProductType) => {
        setTypeToDelete(type)
        setIsDeleteDialogOpen(true)
    }

    const handleDelete = async () => {
        if (!typeToDelete) return

        try {
            await api.deleteProductType(typeToDelete.type_id)
            toast({
                title: "Type Deleted",
                description: `"${typeToDelete.name}" has been removed`,
            })
            setIsDeleteDialogOpen(false)
            setTypeToDelete(null)
            fetchTypes()
        } catch (error: any) {
            toast({
                title: "Delete Failed",
                description: error.message || "Unable to delete this type",
                variant: "destructive"
            })
        }
    }

    return (
        <AuthGuard>
            <div className="container mx-auto px-4 py-8 max-w-6xl">
                <div className="mb-8">
                    <h1 className="text-4xl font-bold mb-3">Product Types Management</h1>
                    <p className="text-muted-foreground text-lg">
                        Manage product categories for your inventory
                    </p>
                </div>

                <Card>
                    <CardHeader>
                        <div className="flex items-center justify-between">
                            <div>
                                <CardTitle>Product Types</CardTitle>
                                <CardDescription>
                                    Create and manage product categories
                                </CardDescription>
                            </div>
                            <Button onClick={() => handleOpenDialog()}>
                                <Plus className="mr-2 h-4 w-4" />
                                Add Type
                            </Button>
                        </div>
                    </CardHeader>
                    <CardContent>
                        {isLoading ? (
                            <div className="flex items-center justify-center py-12">
                                <Loader2 className="h-8 w-8 animate-spin text-muted-foreground" />
                            </div>
                        ) : types.length === 0 ? (
                            <div className="flex flex-col items-center justify-center py-12 text-center">
                                <div className="h-16 w-16 rounded-full bg-muted flex items-center justify-center mb-4">
                                    <Package className="h-8 w-8 text-muted-foreground" />
                                </div>
                                <h3 className="text-lg font-semibold mb-2">No Product Types</h3>
                                <p className="text-sm text-muted-foreground mb-4">
                                    Get started by creating your first product type
                                </p>
                                <Button onClick={() => handleOpenDialog()}>
                                    <Plus className="mr-2 h-4 w-4" />
                                    Add Type
                                </Button>
                            </div>
                        ) : (
                            <Table>
                                <TableHeader>
                                    <TableRow>
                                        <TableHead>Type Name</TableHead>
                                        <TableHead>Products Using</TableHead>
                                        <TableHead>Created</TableHead>
                                        <TableHead className="text-right">Actions</TableHead>
                                    </TableRow>
                                </TableHeader>
                                <TableBody>
                                    {types.map((type) => (
                                        <TableRow key={type.type_id}>
                                            <TableCell className="font-medium">{type.name}</TableCell>
                                            <TableCell>
                                                <span className="inline-flex items-center rounded-full bg-primary/10 px-2.5 py-0.5 text-xs font-medium text-primary">
                                                    {type.product_count} {type.product_count === 1 ? 'product' : 'products'}
                                                </span>
                                            </TableCell>
                                            <TableCell className="text-muted-foreground">
                                                {new Date(type.created_at).toLocaleDateString()}
                                            </TableCell>
                                            <TableCell className="text-right">
                                                <div className="flex justify-end gap-1">
                                                    <Button
                                                        variant="ghost"
                                                        size="icon"
                                                        onClick={() => handleOpenDialog(type)}
                                                    >
                                                        <Edit className="h-4 w-4" />
                                                    </Button>
                                                    <Button
                                                        variant="ghost"
                                                        size="icon"
                                                        onClick={() => handleDeleteClick(type)}
                                                        disabled={type.product_count > 0}
                                                    >
                                                        <Trash2 className="h-4 w-4 text-destructive" />
                                                    </Button>
                                                </div>
                                            </TableCell>
                                        </TableRow>
                                    ))}
                                </TableBody>
                            </Table>
                        )}
                    </CardContent>
                </Card>

                {/* Add/Edit Dialog */}
                <Dialog open={isDialogOpen} onOpenChange={setIsDialogOpen}>
                    <DialogContent>
                        <DialogHeader>
                            <DialogTitle>
                                {editingType ? 'Edit Product Type' : 'Add Product Type'}
                            </DialogTitle>
                            <DialogDescription>
                                {editingType
                                    ? 'Update the product type name. All products using this type will be updated.'
                                    : 'Create a new product type for categorizing your inventory.'}
                            </DialogDescription>
                        </DialogHeader>
                        <div className="space-y-4 py-4">
                            <div className="space-y-2">
                                <Label htmlFor="type-name">Type Name</Label>
                                <Input
                                    id="type-name"
                                    value={typeName}
                                    onChange={(e) => setTypeName(e.target.value)}
                                    placeholder="e.g., Electronics, Clothing, Food"
                                    onKeyDown={(e) => {
                                        if (e.key === 'Enter') {
                                            handleSave()
                                        }
                                    }}
                                />
                            </div>
                        </div>
                        <DialogFooter>
                            <Button variant="outline" onClick={handleCloseDialog}>
                                Cancel
                            </Button>
                            <Button onClick={handleSave} disabled={isSaving}>
                                {isSaving ? (
                                    <>
                                        <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                                        Saving...
                                    </>
                                ) : (
                                    editingType ? 'Update' : 'Create'
                                )}
                            </Button>
                        </DialogFooter>
                    </DialogContent>
                </Dialog>

                {/* Delete Confirmation Dialog */}
                <AlertDialog open={isDeleteDialogOpen} onOpenChange={setIsDeleteDialogOpen}>
                    <AlertDialogContent>
                        <AlertDialogHeader>
                            <AlertDialogTitle>Delete {typeToDelete?.name}?</AlertDialogTitle>
                            <AlertDialogDescription>
                                This action cannot be undone. This will permanently delete the product type.
                                {typeToDelete && typeToDelete.product_count > 0 && (
                                    <span className="block mt-2 text-destructive font-medium">
                                        Cannot delete: {typeToDelete.product_count} product(s) are using this type.
                                    </span>
                                )}
                            </AlertDialogDescription>
                        </AlertDialogHeader>
                        <AlertDialogFooter>
                            <AlertDialogCancel>Cancel</AlertDialogCancel>
                            <AlertDialogAction
                                onClick={handleDelete}
                                className="bg-destructive text-destructive-foreground hover:bg-destructive/90"
                                disabled={typeToDelete ? typeToDelete.product_count > 0 : false}
                            >
                                Delete Type
                            </AlertDialogAction>
                        </AlertDialogFooter>
                    </AlertDialogContent>
                </AlertDialog>
            </div>
        </AuthGuard>
    )
}
