# Reference Asset: `resources/component-template.tsx`

Converted to Markdown for Gemini Web upload compatibility.

````tsx
import React from 'react';
import { View, StyleSheet } from 'react-native';

export interface StitchComponentProps {
  readonly children?: React.ReactNode;
  readonly testID?: string;
}

export const StitchComponent: React.FC<StitchComponentProps> = ({
  children,
  testID,
}) => {
  return (
    <View style={styles.container} testID={testID} accessibilityRole="none">
      {children}
    </View>
  );
};

const styles = StyleSheet.create({
  container: {},
});

export default StitchComponent;

````
