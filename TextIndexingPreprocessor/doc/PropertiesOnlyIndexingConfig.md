# PropertiesOnlyIndexingHandler - Building the JAR

This document describes how to build the JAR file for the PropertiesOnlyIndexingHandler sample.

## Overview

The [`PropertiesOnlyIndexingHandler.java`](../src/com/ibm/ecm/sample/textindexpreprocessor/PropertiesOnlyIndexingHandler.java) is a Text Indexing Preprocessor that skips content extraction and only indexes document properties. The handler implements the `TextIndexingPreprocessor` interface and sets the extraction result to null with `NO_TEXT_EXTRACTED` status, effectively skipping content indexing while allowing property-based indexing to proceed normally.

## How It Works

The handler performs the following operations:

1. **Validates** that the source object is a Document instance
2. **Logs** processing activity using `HandlerCallContext` for trace logging
3. **Sets** the extraction result to null with `IndexingFailureCode.NO_TEXT_EXTRACTED_AS_INT`
4. **Returns** `true` to indicate successful processing

By setting the extraction result to null, the handler instructs Content Engine to skip text extraction from document content while continuing with property-based indexing normally.

## Building the JAR File

### Prerequisites

- Java Development Kit (JDK) 8 or later
- Access to FileNet Content Engine API libraries (`Jace.jar`)

### Build Steps

1. **Locate the Content Engine API libraries**

   Find `Jace.jar` on your Content Engine server, typically in:
   ```
   /opt/IBM/FileNet/ContentEngine/lib/Jace.jar
   ```

2. **Create the package directory structure**

   ```bash
   mkdir -p com/ibm/ecm/sample/textindexpreprocessor
   ```

3. **Copy the source file**

   ```bash
   cp PropertiesOnlyIndexingHandler.java com/ibm/ecm/sample/textindexpreprocessor/
   ```

4. **Compile the source**

   Using a specific JAR:
   ```bash
   javac -cp /path/to/Jace.jar com/ibm/ecm/sample/textindexpreprocessor/PropertiesOnlyIndexingHandler.java
   ```

   Or using all JARs in a directory:
   ```bash
   javac -cp "/path/to/content-engine/lib/*" com/ibm/ecm/sample/textindexpreprocessor/PropertiesOnlyIndexingHandler.java
   ```

5. **Create the JAR file**

   ```bash
   jar cf PropertiesOnlyIndexingHandler.jar -C . com/ibm/ecm/sample/textindexpreprocessor/PropertiesOnlyIndexingHandler.class
   ```

### Verify the JAR

Check the JAR contents:

```bash
jar tf PropertiesOnlyIndexingHandler.jar
```

Expected output:
```
META-INF/
META-INF/MANIFEST.MF
com/
com/ibm/
com/ibm/ecm/
com/ibm/ecm/sample/
com/ibm/ecm/sample/textindexpreprocessor/
com/ibm/ecm/sample/textindexpreprocessor/PropertiesOnlyIndexingHandler.class
```

## Configuration in ACCE

After building and deploying the JAR file to your Content Engine server's classpath:

1. Log in to ACCE (Administration Console for Content Platform Engine)
2. Navigate to your target Object Store
3. Expand **Data Design > Classes > Document**
4. Select the Document class where you want to apply properties-only indexing
5. In the **Actions** tab, click **New Action**
6. Configure the action:
   - **Action Type**: Text Indexing Preprocessor Action
   - **Display Name**: Properties Only Indexing
   - **Handler Class Name**: `com.ibm.ecm.sample.textindexpreprocessor.PropertiesOnlyIndexingHandler`
   - **Enabled**: Check this box
7. Click **Next**, review settings, and click **Finish**
8. Click **Save**

## Additional Resources

- [IBM FileNet P8 Platform Documentation](https://www.ibm.com/docs/en/content-cortex)
- [Text Indexing Preprocessors](https://www.ibm.com/docs/en/content-cortex/26.0.0?topic=objects-text-indexing-preprocessors)
- [Working with Text Indexing Preprocessors](https://www.ibm.com/docs/en/content-cortex/26.0.0?topic=preprocessors-working-text-indexing)
- [Content Platform Engine API Documentation](https://www.ibm.com/docs/en/content-cortex/26.0.0?topic=development-content-engine-java-api-reference)
- [Interface TextIndexingPreprocessor](https://www.ibm.com/docs/en/content-cortex/26.0.0?topic=comfilenetapiengine-textindexingpreprocessor)