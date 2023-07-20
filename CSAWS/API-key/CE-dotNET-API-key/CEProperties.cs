/*
 * Licensed Materials - Property of IBM (c) Copyright IBM Corp. 2023 All Rights Reserved.
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
using System;
using System.Collections.Generic;
using System.IO;
using System.Text.RegularExpressions;

public class CEProperties
{
    // Define the property names that clients may make use of
    public const string APIC_TOKEN = "APIC_Token";
    public const string APIC_TOKEN_URI = "APIC_URI";
    public const string APIC_CLIENT_ID = "APIC_ClientId";
    public const string APIC_CLIENT_SECRET = "APIC_ClientSecret";
    public const string CE_URL = "CE_URL";
    public const string CE_CONTENT_PATH = "CE_ContentPath";
    public const string CE_DOWNLOAD_FOLDER = "CE_DownloadFolder";

    // Java properties class does the real work
    private const string PROPERTIES_RESOURCE = "cejavaapikey.properties";
    private static readonly Dictionary<string, string> properties = new Dictionary<string, string>();

    // Constructor
    public CEProperties(string name)
    {
        if (properties.Count == 0)
        {
            InitializeProperties(name);
        }
    }

    /**
     * @param defaultValue   Default value to return if the property is not found
     * @param property       Property or key
     * @return The value for the key given or the defaultValue specified
     */
    public string Get(string property, string defaultValue)
    {
        if (properties.TryGetValue(property, out string value))
        {
            return value;
        }
        return defaultValue;
    }

    /**
     * @param property   Property or key
     * @return The value for the key given
     */
    public string Get(string property)
    {
        return Get(property, null);
    }

    /**
     * @param property   Property or key
     * @return The int value for the key given
     */
    public int GetInt(string property)
    {
        string value = Get(property);
        if (!string.IsNullOrEmpty(value) && int.TryParse(value, out int intValue))
        {
            return Math.Max(intValue, 0);
        }
        return 0;
    }

    /**
     * @param property   Property or key
     * @return The date value for the key given
     */
    public DateTime? GetDate(string property)
    {
        string value = Get(property);
        if (!string.IsNullOrEmpty(value))
        {
            if (DateTime.TryParseExact(value, "MM/dd/yyyy", null, System.Globalization.DateTimeStyles.None, out DateTime dateValue))
            {
                return dateValue;
            }
            else
            {
                Console.Error.WriteLine($"Failed to parse value [{value}] for property [{property}]");
            }
        }
        return null;
    }

    // Open the properties file
    private void InitializeProperties(string name)
    {
        if (properties.Count == 0)
        {
            bool found = false;
            string fileName = string.IsNullOrEmpty(name) ? PROPERTIES_RESOURCE : name;
            string filePath = Path.Combine(Environment.CurrentDirectory, fileName);
            
            // First try loading from the current working directory
            if (File.Exists(filePath))
            {
                try
                {
                    using (FileStream fs = new FileStream(filePath, FileMode.Open, FileAccess.Read))
                    {
                        LoadProperties(fs);
                        found = true;
                    }
                }
                catch (IOException ex)
                {
                    Console.Error.WriteLine("IO exception CEjavaAPIkey.properties file CEproperties.initializeProperties");
                    Console.Error.WriteLine(ex.Message);
                }
            }

            // If that didn't work, try loading from classpath
            if (!found)
            {
                using (Stream stream = typeof(CEProperties).Assembly.GetManifestResourceStream($"{typeof(CEProperties).Namespace}.{fileName}"))
                {
                    if (stream != null)
                    {
                        LoadProperties(stream);
                        found = true;
                    }
                }
            }

            // No penalty having empty properties file...
            if (properties.Count == 0)
                properties["dummy"] = "dummy";
        }
    }

    private void LoadProperties(Stream stream)
    {
        using (StreamReader reader = new StreamReader(stream))
        {
            string line;
            while ((line = reader.ReadLine()) != null)
            {
                line = line.Trim();
                if (line.Length > 0 && !line.StartsWith("#"))
                {
                    int equalsIndex = line.IndexOf('=');
                    if (equalsIndex > 0 && equalsIndex < line.Length - 1)
                    {
                        string key = line.Substring(0, equalsIndex).Trim();
                        string value = line.Substring(equalsIndex + 1).Trim();
                        properties[key] = value;
                    }
                }
            }
        }
    }
}
