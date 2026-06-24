# Text Indexing Preprocessor sample code

The Content Platform Engine provides a Text Indexing Preprocessor interface that allows custom plugins to control how document content is indexed. This feature enables developers to customize the text extraction and indexing behavior for documents.

As part of this sample, a properties-only indexing handler is provided which skips content extraction and only indexes document properties.

## PropertiesOnlyIndexingHandler

The `PropertiesOnlyIndexingHandler` is a simplified text indexing preprocessor that ignores content extraction and only indexes document properties. This handler sets the extraction result to null, effectively skipping content indexing while allowing property-based indexing to proceed normally.

### Use Cases

This handler is useful when:
- You want to index documents based on metadata only, without extracting text from content
- Content extraction is unnecessary or too resource-intensive for certain document classes
- You need to improve indexing performance by skipping content processing
- Documents contain sensitive content that should not be indexed

### Contents of this sample component

This sample contains the following:

- The source for the sample handler [`PropertiesOnlyIndexingHandler.java`](src/com/ibm/ecm/sample/textindexpreprocessor/PropertiesOnlyIndexingHandler.java)
- A document describing how to build the JAR file [`PropertiesOnlyIndexingConfig.md`](doc/PropertiesOnlyIndexingConfig.md)
- The compiled version of the sample handler [`PropertiesOnlyIndexingHandler.jar`](files/PropertiesOnlyIndexingHandler.jar)

### Building and Configuration

To build and use this handler:

1. Build the JAR file using the instructions in the [configuration guide](doc/PropertiesOnlyIndexingConfig.md)
2. In ACCE (Administration Console for Content Platform Engine), create a Text Indexing Preprocessor Action
3. Set the `HandlerClassName` to `com.ibm.ecm.sample.textindexpreprocessor.PropertiesOnlyIndexingHandler`
4. Associate the action with the desired Document Class(es)

For detailed build and configuration instructions, see the [configuration guide](doc/PropertiesOnlyIndexingConfig.md).

### How It Works

The handler implements the `TextIndexingPreprocessor` interface and:
1. Validates that the source object is a Document
2. Logs the processing activity using `HandlerCallContext`
3. Sets the extraction result to null with status `NO_TEXT_EXTRACTED`
4. Returns `true` to indicate successful processing

This allows the indexing process to continue with property-based indexing while skipping content extraction.