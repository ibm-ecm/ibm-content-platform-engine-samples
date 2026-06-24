/*
 * Licensed Materials - Property of IBM (c) Copyright IBM Corp. 2026 All Rights Reserved.
 * 
 * US Government Users Restricted Rights - Use, duplication or disclosure restricted by GSA ADP Schedule Contract with
 * IBM Corp.
 * 
 * DISCLAIMER OF WARRANTIES :
 * 
 * Permission is granted to copy and modify this Sample code, and to distribute modified versions provided that both the
 * copyright notice, and this permission notice and warranty disclaimer appear in all copies and modified versions.
 * 
 * THIS SAMPLE CODE IS LICENSED TO YOU AS-IS. IBM AND ITS SUPPLIERS AND LICENSORS DISCLAIM ALL WARRANTIES, EITHER
 * EXPRESS OR IMPLIED, IN SUCH SAMPLE CODE, INCLUDING THE WARRANTY OF NON-INFRINGEMENT AND THE IMPLIED WARRANTIES OF
 * MERCHANTABILITY OR FITNESS FOR A PARTICULAR PURPOSE. IN NO EVENT WILL IBM OR ITS LICENSORS OR SUPPLIERS BE LIABLE FOR
 * ANY DAMAGES ARISING OUT OF THE USE OF OR INABILITY TO USE THE SAMPLE CODE, DISTRIBUTION OF THE SAMPLE CODE, OR
 * COMBINATION OF THE SAMPLE CODE WITH ANY OTHER CODE. IN NO EVENT SHALL IBM OR ITS LICENSORS AND SUPPLIERS BE LIABLE
 * FOR ANY LOST REVENUE, LOST PROFITS OR DATA, OR FOR DIRECT, INDIRECT, SPECIAL, CONSEQUENTIAL, INCIDENTAL OR PUNITIVE
 * DAMAGES, HOWEVER CAUSED AND REGARDLESS OF THE THEORY OF LIABILITY, EVEN IF IBM OR ITS LICENSORS OR SUPPLIERS HAVE
 * BEEN ADVISED OF THE POSSIBILITY OF SUCH DAMAGES.
 */

package com.ibm.ecm.sample.textindexpreprocessor;

import java.util.Map;
import java.util.Set;

import com.filenet.api.admin.CmTextIndexingPreprocessorAction;
import com.filenet.api.constants.IndexingFailureCode;
import com.filenet.api.core.Document;
import com.filenet.api.core.IndependentlyPersistableObject;
import com.filenet.api.engine.HandlerCallContext;
import com.filenet.api.engine.TextIndexingPreprocessor;
import com.filenet.api.engine.TextIndexingPreprocessorServices;
import com.filenet.api.engine.TextIndexingPreprocessorServices.TextExtractionResult;

/**
 * A simplified text indexing preprocessor that ignores content extraction
 * and only indexes document properties. This handler sets the result to null,
 * effectively skipping content indexing while allowing property-based indexing
 * to proceed normally.
 *
 * <p><b>Usage:</b> Configure this handler in ACCE by creating a Text Indexing
 * Preprocessor Action with HandlerClassName set to
 * {@code com.ibm.ecm.sample.textindexpreprocessor.PropertiesOnlyIndexingHandler}, then
 * associate it with a Document Class.</p>
 */
public class PropertiesOnlyIndexingHandler implements TextIndexingPreprocessor
{
    public String getOutputContentType()
    {
        return "text/plain";
    }
    
    public boolean preprocess (
                    CmTextIndexingPreprocessorAction action,
                    TextIndexingPreprocessorServices services,
                    IndependentlyPersistableObject sourceObject,
                    Map<String,Set<String>> fields,
                    TextExtractionResult result )
    {
        HandlerCallContext hcc = HandlerCallContext.getInstance();
        
        // Validate source object type
        if ( !(sourceObject instanceof Document) )
        {
            String className = sourceObject != null ? sourceObject.getClassName() : "null";
            hcc.logWarning("Properties-only indexing handler, unexpected call for object of class " +
                          className);
            return false;
        }

        Document sourceDoc = (Document)sourceObject;
        
        if ( hcc.isSummaryTraceEnabled() )
        {
            hcc.traceSummary("Properties-only indexing handler, processing document " +
                            sourceDoc.get_Id() + ", ignoring content");
        }
        
        if ( hcc.isDetailTraceEnabled() )
        {
            hcc.traceDetail("Properties-only indexing handler, entering for " +
                           sourceDoc.get_Id());
            hcc.traceDetail("Properties-only indexing handler, action=" +
                           (action != null ? action.get_DisplayName() : "null") +
                           ", document class=" + sourceDoc.getClassName());
            
            if ( fields != null && !fields.isEmpty() )
            {
                hcc.traceDetail("Properties-only indexing handler, number of fields=" +
                               fields.size());
            }
        }
        
        result.setResult ( null, IndexingFailureCode.NO_TEXT_EXTRACTED_AS_INT, null );
        
        if ( hcc.isSummaryTraceEnabled() )
        {
            hcc.traceSummary("Properties-only indexing handler, completed for document " +
                            sourceDoc.get_Id() + ", properties indexed, content ignored");
        }
        
        if ( hcc.isDetailTraceEnabled() )
        {
            hcc.traceDetail("Properties-only indexing handler, result set with status=" +
                           IndexingFailureCode.NO_TEXT_EXTRACTED_AS_INT +
                           " (NO_TEXT_EXTRACTED)");
        }
        
        return true;
    }
}
