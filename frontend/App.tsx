import React from 'react';
import { NavigationContainer } from '@react-navigation/native';
import { createStackNavigator } from '@react-navigation/stack';
import LoginScreen from './src/screens/LoginScreen';
import RegisterScreen from './src/screens/RegisterScreen';
import PlansScreen from './src/screens/PlansScreen';
import CreatePlanScreen from './src/screens/CreatePlanScreen';
import ExercisesScreen from './src/screens/ExercisesScreen';
import CreateExerciseScreen from './src/screens/CreateExerciseScreen';

const Stack = createStackNavigator();

export default function App() {
  return (
    <NavigationContainer>
      <Stack.Navigator initialRouteName="Login">
        <Stack.Screen 
          name="Login" 
          component={LoginScreen} 
          options={{ title: 'Login' }}
        />
        <Stack.Screen 
          name="Register" 
          component={RegisterScreen} 
          options={{ title: 'Register' }}
        />
        <Stack.Screen 
          name="Main" 
          component={PlansScreen} 
          options={{ 
            title: 'My Plans',
            headerLeft: () => null
          }}
        />
        <Stack.Screen 
          name="CreatePlan" 
          component={CreatePlanScreen} 
          options={{ title: 'Create Plan' }}
        />
        <Stack.Screen 
          name="Exercises" 
          component={ExercisesScreen} 
          options={{ title: 'Exercises' }}
        />
        <Stack.Screen 
          name="CreateExercise" 
          component={CreateExerciseScreen} 
          options={{ title: 'Create Exercise' }}
        />
      </Stack.Navigator>
    </NavigationContainer>
  );
}
