import React, { useState } from "react"

const UserInput = () => {
  const [preferences, setPreferences] = useState("")
  const [ingredients, setIngredients] = useState("")

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    console.log("Dietary Preferences:", preferences)
    console.log("Ingredients:", ingredients)
    setPreferences("")
    setIngredients("")
  }

  return (
    <form
      onSubmit={handleSubmit}
      className="max-w-md mx-auto p-4 bg-white shadow-md rounded-lg"
    >
      <div className="mb-4">
        <label className="block text-gray-700 text-sm font-bold mb-2">
          Dietary Preferences:
        </label>
        <input
          type="text"
          value={preferences}
          onChange={(e) => setPreferences(e.target.value)}
          placeholder="e.g., vegan, gluten-free"
          className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
        />
      </div>
      <div className="mb-4">
        <label className="block text-gray-700 text-sm font-bold mb-2">
          Ingredients:
        </label>
        <input
          type="text"
          value={ingredients}
          onChange={(e) => setIngredients(e.target.value)}
          placeholder="e.g., tomato, spinach, garlic"
          className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
        />
      </div>
      <button
        type="submit"
        className="bg-purple-500 hover:bg-yellow-500 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline"
      >
        Get Recipes!
      </button>
    </form>
  )
}

export default UserInput
